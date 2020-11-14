import os
from pyhocon import ConfigFactory

MAIN_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(MAIN_FOLDER, 'application.conf')

config = ConfigFactory.parse_file(CONFIG_FILE)
token = config.get_string("telegram_token")
channel = config.get_string("telegram_channel")
tracking_params = config.get_string("tracking_params")
