"""Constants of the ShinHu Gas Fee component."""

DEFAULT_NAME = "ShinHu Gas Fee"
DEFAULT_NAME_UPLOAD_USAGE = "ShinHu Gas Upload Usage"
DOMAIN = "shinhugas_fee"
DOMAINS = [ "sensor", "binary_sensor" ]
DATA_KEY = "sensor.shinhugas_fee"
DATA_KEY_BINARY = "binary_sensor.shinhu_gas_upload_usage"

ATTR_BILLING_MONTH = "billing_month"
ATTR_CURRENT_GASMETER = "current_gasmeter"
ATTR_PAYMENT = "gas_payment"
ATTR_GAS_CONSUMPTION = "gas_consumption"
ATTR_EXTRA_GAS = "extra_gas"
ATTR_BILL_AMOUNT = "billing_amount"
ATTR_HTTPS_RESULT = "https_result"
ATTR_UPLOAD_DATETIME = "upload_datetime"
ATTR_USAGE = "usage"
ATTR_LIST = [
    ATTR_BILLING_MONTH,
    ATTR_CURRENT_GASMETER,
    ATTR_PAYMENT,
    ATTR_GAS_CONSUMPTION,
    ATTR_EXTRA_GAS,
    ATTR_BILL_AMOUNT,
    ATTR_HTTPS_RESULT
]

CONF_GASID = "gasid"
CONF_COOKIE = "cookie"
# 5308 characters
CONF_VIEWSTATE = "viewstate"
# 668 characters
CONF_VIEWSTATEGENERATOR = "viewstategenerator"
# 636 characters
CONF_VIEWSTATE4UPLOAD = "viewstate4upload"
ATTRIBUTION = "Powered by ShinHu Gas Data"
MANUFACTURER = "ShinHu Gas"

HA_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 OPR/38.0.2220.41"
BASE_URL = 'http://61.222.127.147/shinhuwww/member_main.aspx'

REQUEST_TIMEOUT = 10  # seconds
