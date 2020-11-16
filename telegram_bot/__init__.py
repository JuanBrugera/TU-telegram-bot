import os

from pyhocon import ConfigFactory

MAIN_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(MAIN_FOLDER, 'application.conf')

config = ConfigFactory.parse_file(CONFIG_FILE)

TOKEN = config.get_string("telegram_token")
CHANNEL = config.get_string("telegram_channel")
TRACKING_PARAMS = config.get_string("tracking_params")
DEVICES = config.get_config("devices")
BUTTONS = config.get_list("button_texts")
TIMEOUT = config.get_int("timeout")
SOCIAL = config.get_config("social")
STOCK_ALERT = config.get_int("stock_alert")
LOG_LEVEL = config.get_int("log.level")
