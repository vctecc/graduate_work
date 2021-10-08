import os
from logging import config as logging_config

from .logger import LOGGING

logging_config.dictConfig(LOGGING)

PROJECT_NAME = os.getenv("PROJECT_NAME", "Payment API")
DEBUG = bool(os.getenv("DEBUG")) or False
