from celery import Celery
from datetime import timedelta

from .config import settings


app = Celery('payment_service', broker=settings.broker_url, include=['tasks'])

if settings.test:
    SCHEDULE = timedelta(seconds=1)
else:
    SCHEDULE = timedelta(seconds=30)

CELERYBEAT_SCHEDULE = {
    'handle_pending_payments': {
        'task': 'handle_pending_payments',
        'schedule': SCHEDULE,
        'options': {'queue': 'payments'},
        'args': tuple(),
    },
}

app.conf.beat_schedule = CELERYBEAT_SCHEDULE
