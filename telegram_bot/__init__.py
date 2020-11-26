import os

from pyhocon import ConfigFactory

MAIN_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(MAIN_FOLDER, 'application.conf')

config = ConfigFactory.parse_file(CONFIG_FILE)

TOKEN = os.getenv('TELEGRAM_TOKEN', config.get_string("telegram_token"))
CHANNEL = os.getenv('TELEGRAM_CHANNEL', config.get_string("telegram_channel"))
TRACKING_PARAMS = config.get_string("tracking_params")
DEVICES = config.get_config("devices")
OFFER_BUTTONS = config.get_list("button_texts.offers")
NORMAL_BUTTONS = config.get_list("button_texts.normal")
TIMEOUT = config.get_int("timeout")
SOCIAL = config.get_config("social")
STOCK_ALERT = config.get_int("stock_alert")
LOG_LEVEL = os.getenv('LOG_LEVEL', config.get_int("log.level"))
LOG_TO_STD = os.getenv('LOG_TO_STD', 'FALSE') == 'TRUE'

IDS = os.getenv('TELEGRAM_IDS', None)
if IDS:
    VALID_IDS = [int(x) for x in IDS.split(',')]   # string with comma separated IDs
else:
    VALID_IDS = config.get_list("valid_ids")
