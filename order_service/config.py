import os
import pathlib
from datetime import timedelta
import logging.config as logging_config

BROKER_URL = os.getenv("CELERY_BROKER_URL", "pyamqp://guest:guest@rabbit//")


CELERYBEAT_SCHEDULE = {
    'get_pending_subscriptions': {
        'task': 'get_pending_subscriptions',
        'schedule': timedelta(seconds=3),
        'args': ()
    },
}

LOGGER_CONFIG = pathlib.Path(__file__).parent / 'logging.conf'
LOGGER_NAME = 'senders'
logging_config.fileConfig(LOGGER_CONFIG)
