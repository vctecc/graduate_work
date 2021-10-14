import os
import pathlib
from datetime import timedelta
import logging.config as logging_config

BROKER_URL = os.getenv("CELERY_BROKER_URL", "pyamqp://guest:guest@rabbit//")

SCHEDULE = timedelta(hours=24)

CELERYBEAT_SCHEDULE = {
    'handle_pending_payments': {
        'task': 'handle_pending_payments',
        'schedule': SCHEDULE,
        'options': {'queue': 'payments'},
        'args': ()
    },
}

LOGGER_CONFIG = pathlib.Path(__file__).parent / 'logging.conf'
LOGGER_NAME = 'order_service'
logging_config.fileConfig(LOGGER_CONFIG)

SUBSCRIPTION_API_URL = os.environ.get("SUBSCRIPTION_API_URL",
                                      "https://31e9ff3d-42ad-467e-9eb6-ccfa680d9f00.mock.pstmn.io/api/v1/")

PAYMENTS_API_URL = os.environ.get("PAYMENTS_API_URL",
                                      "https://31e9ff3d-42ad-467e-9eb6-ccfa680d9f00.mock.pstmn.io/api/v1/")
