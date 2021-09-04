"""Config flow to configure ShinHu Gas Fee component."""
from collections import OrderedDict
from typing import Optional
import voluptuous as vol

from homeassistant.config_entries import (
    CONN_CLASS_LOCAL_PUSH,
    ConfigFlow,
    OptionsFlow,
    ConfigEntry
    )
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.typing import ConfigType
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CONF_GASID,
    CONF_VIEWSTATE,
    CONF_VIEWSTATEGENERATOR,
    CONF_VIEWSTATE4UPLOAD
)

class ShinHuFlowHandler(ConfigFlow, domain=DOMAIN):
    """Handle a ShinHu Gas Fee config flow."""

    VERSION = 1
    CONNECTION_CLASS = CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize flow."""
        self._gas_id: Optional[str] = None
        self._viewstate: Optional[str] = None
        self._viewstategenerator: Optional[str] = None
        self._viewstate4upload: Optional[str] = None

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry):
        """ get option flow """
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self,
        user_input: Optional[ConfigType] = None,
        error: Optional[str] = None
    ):  # pylint: disable=arguments-differ
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self._set_user_input(user_input)
            self._name = user_input.get(CONF_GASID)
            unique_id = self._gas_id
            await self.async_set_unique_id(unique_id)
            return self._async_get_entry()

        fields = OrderedDict()
        fields[vol.Required(CONF_GASID,
                            default=self._gas_id or vol.UNDEFINED)] = str
        fields[vol.Required(CONF_VIEWSTATE,
                            default=self._viewstate or vol.UNDEFINED)] = str
        fields[vol.Required(CONF_VIEWSTATEGENERATOR,
                            default=self._viewstategenerator or vol.UNDEFINED)] = str
        fields[vol.Optional(CONF_VIEWSTATE4UPLOAD,
                            default=self._viewstate4upload or vol.UNDEFINED)] = str
        self._name = self._gas_id
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(fields),
            errors={'base': error} if error else None
        )

    @property
    def _name(self):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        return self.context.get(CONF_NAME)

    @_name.setter
    def _name(self, value):
        # pylint: disable=no-member
        # https://github.com/PyCQA/pylint/issues/3167
        self.context[CONF_NAME] = value
        self.context["title_placeholders"] = {"name": self._name}

    def _set_user_input(self, user_input):
        if user_input is None:
            return
        self._gas_id = user_input.get(CONF_GASID, "")
        self._viewstate = user_input.get(CONF_VIEWSTATE, "")
        self._viewstategenerator = user_input.get(CONF_VIEWSTATEGENERATOR, "")
        self._viewstate4upload = user_input.get(CONF_VIEWSTATE4UPLOAD, "")

    @callback
    def _async_get_entry(self):
        return self.async_create_entry(
            title=self._name,
            data={
                CONF_GASID: self._gas_id,
                CONF_VIEWSTATE: self._viewstate,
                CONF_VIEWSTATEGENERATOR: self._viewstategenerator,
                CONF_VIEWSTATE4UPLOAD: self._viewstate4upload
            },
        )


class OptionsFlowHandler(OptionsFlow):
    # pylint: disable=too-few-public-methods
    """Handle options flow changes."""
    _gas_id = None
    _cookie = None
    _viewstate = None
    _viewstategenerator = None
    _viewstate4upload = None

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage options."""
        if user_input is not None:
            self._viewstategenerator = user_input.get(CONF_VIEWSTATEGENERATOR)
            self._viewstate4upload = user_input.get(CONF_VIEWSTATE4UPLOAD)
            self._gas_id = user_input.get(CONF_GASID)
            self._viewstate = user_input.get(CONF_VIEWSTATE)
            return self.async_create_entry(
                title='',
                data={
                    CONF_GASID: self._gas_id,
                    CONF_VIEWSTATE: self._viewstate,
                    CONF_VIEWSTATEGENERATOR: self._viewstategenerator,
                    CONF_VIEWSTATE4UPLOAD: self._viewstate4upload
                },
            )
        self._gas_id = self.config_entry.options.get(CONF_GASID, '')
        self._viewstate = self.config_entry.options.get(CONF_VIEWSTATE, '')
        self._viewstategenerator = self.config_entry.options.get(CONF_VIEWSTATEGENERATOR, '')
        self._viewstate4upload = self.config_entry.options.get(CONF_VIEWSTATE4UPLOAD, '')

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_GASID, default=self._gas_id): str,
                    vol.Required(CONF_VIEWSTATE, default=self._viewstate): str,
                    vol.Required(CONF_VIEWSTATEGENERATOR, default=self._viewstategenerator): str,
                    vol.Optional(CONF_VIEWSTATE4UPLOAD, default=self._viewstate4upload): str
                }
            ),
        )
