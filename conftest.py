import logging
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)

logging.getLogger('urllib3').setLevel(logging.WARNING)
