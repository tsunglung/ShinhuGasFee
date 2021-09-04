"""Upload Gas Usage binary sensor instances."""
import asyncio
import logging
import voluptuous as vol
from aiohttp.hdrs import USER_AGENT
import requests
from functools import partial
from bs4 import BeautifulSoup

from homeassistant.components.binary_sensor import BinarySensorEntity
import homeassistant.util.dt as dt_util
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    ATTR_ENTITY_ID,
    HTTP_OK,
    HTTP_FORBIDDEN,
    HTTP_NOT_FOUND,
)
#from . import setup_input
from .const import (
    ATTR_HTTPS_RESULT,
    ATTR_UPLOAD_DATETIME,
    ATTR_USAGE,
    BASE_URL,
    CONF_GASID,
    CONF_VIEWSTATE4UPLOAD,
    CONF_VIEWSTATEGENERATOR,
    DEFAULT_NAME_UPLOAD_USAGE,
    DOMAIN,
    DATA_KEY_BINARY,
    HA_USER_AGENT,
    MANUFACTURER,
    REQUEST_TIMEOUT
)


_LOGGER = logging.getLogger(DOMAIN)

SERVICE_GAS_UPLOAD_USAGE = "gas_upload_usage"

GAS_SERVICE_SCHEMA = vol.Schema({vol.Optional(ATTR_ENTITY_ID): cv.entity_ids})

SERVICE_SCHEMA_UPLOAD_USAGE = GAS_SERVICE_SCHEMA.extend(
    {vol.Required(ATTR_USAGE): vol.All(vol.Coerce(int), vol.Clamp(min=0, max=9999))}
)

SERVICE_TO_METHOD = {
    SERVICE_GAS_UPLOAD_USAGE: {
        "method": "async_upload_gas_usage",
        "schema": SERVICE_SCHEMA_UPLOAD_USAGE,
    }
}


async def async_setup_entry(hass, config, async_add_devices):
    """Set up the binary sensors from a config entry."""
    if DATA_KEY_BINARY not in hass.data:
        hass.data[DATA_KEY_BINARY] = {}

#    binary_sensors = [DEFAULT_NAME_UPLOAD_USAGE]

    if config.data.get(CONF_GASID, None):
        gasid = config.data[CONF_GASID]
        viewstate4upload = config.data.get(CONF_VIEWSTATE4UPLOAD, None)
        viewstategenerator = config.data[CONF_VIEWSTATEGENERATOR]
    else:
        gasid = config.options[CONF_GASID]
        viewstate4upload = config.options.get(CONF_VIEWSTATE4UPLOAD, None)
        viewstategenerator = config.options[CONF_VIEWSTATEGENERATOR]

    device = GasUsageUploadBinarySensor(hass, gasid, viewstate4upload, viewstategenerator)

    hass.data[DATA_KEY_BINARY][config.entry_id] = device
    async_add_devices([device], update_before_add=True)

    async def async_service_handler(service):
        """Map services to methods on Gas Fee."""
        method = SERVICE_TO_METHOD.get(service.service)
        params = {
            key: value for key, value in service.data.items() if key != ATTR_ENTITY_ID
        }

        entity_ids = service.data.get(ATTR_ENTITY_ID)
        if entity_ids:
            devices = [
                device
                for device in hass.data[DATA_KEY_BINARY].values()
                if device.entity_id in entity_ids
            ]
        else:
            devices = hass.data[DATA_KEY_BINARY].values()
        update_tasks = []
        for device in devices:
            if not hasattr(device, method["method"]):
                continue
            await getattr(device, method["method"])(**params)
            update_tasks.append(device.async_update_ha_state(True))

        if update_tasks:
            await asyncio.wait(update_tasks)

    for gas_upload_service in SERVICE_TO_METHOD:
        schema = SERVICE_TO_METHOD[gas_upload_service].get(
            "schema", GAS_SERVICE_SCHEMA
        )
        hass.services.async_register(
            DOMAIN, gas_upload_service, async_service_handler, schema=schema
        )

class GasUsageUploadBinarySensor(BinarySensorEntity):
    """Represent a binary sensor."""

    def __init__(self, hass, gasid, viewstate4upload, viewstategenerator):
        """Set initializing values."""
        super().__init__()
        self._name = "{} {}".format(DEFAULT_NAME_UPLOAD_USAGE, gasid)
        self._attributes = {}
        self._state = False
        self._gasid = gasid
        self._viewstate4upload = viewstate4upload
        self._viewstategenerator = viewstategenerator
        self._https_result = None
        self._upload_datetime = None
        self.hass = hass
        self.uri = BASE_URL

    @property
    def unique_id(self):
        """Return an unique ID."""
        return self._name

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""
        self._attributes[ATTR_HTTPS_RESULT] = self._https_result
        self._attributes[ATTR_UPLOAD_DATETIME] = self._upload_datetime
        return self._attributes

    @property
    def device_info(self):
        """Return Device Info."""
        return {
            'identifiers': {(DOMAIN, self._gasid)},
            'manufacturer': MANUFACTURER,
            'name': self._name
        }

    def _parser_html(self, text):
        """Return parsing HTML."""
        soup = BeautifulSoup(text, 'html.parser')
        for result in soup.findAll("script"):
            if "新增自報度數成功!!" in result.string:
                return True
        return False

    async def async_upload_gas_usage(self, usage: int = 0):
        """Upload Gas Usage."""

        _LOGGER.error(usage)
        if self._viewstate4upload is None or self._viewstategenerator is None:
            _LOGGER.error("The token can not empty!")
            return
        headers = {USER_AGENT: HA_USER_AGENT}
        payload = {
            "__VIEWSTATE": self._viewstate4upload,
            "__VIEWSTATEGENERATOR": self._viewstategenerator,
            "Ddl_telrel": self._gasid,
            "Txt_telrel": usage,
            "txt_telrel_mark": "",
            "Button11": "確定"
        }

        try:
            self._upload_datetime = dt_util.now()
            req = await self.hass.async_add_executor_job(
                partial(
                    requests.post,
                    self.uri,
                    headers=headers,
                    data=payload,
                    timeout=REQUEST_TIMEOUT
                    )
                )

        except requests.exceptions.RequestException:
            _LOGGER.error("Failed fetching data for %s", self._gasid)
            return

        self._https_result = req.status_code
        if req.status_code == HTTP_OK:
            self._state = self._parser_html(req.text)
        elif req.status_code == HTTP_NOT_FOUND:
            self._state = False
        else:
            info = ""
            if req.status_code == HTTP_FORBIDDEN:
                info = " Token or Cookie is expired"
            _LOGGER.error(
                "Failed fetching data for %s (HTTP Status_code = %d).%s",
                self._gasid,
                req.status_code,
                info
            )
