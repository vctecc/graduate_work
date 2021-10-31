from datetime import timedelta

from celery import Celery

from .config import settings

app = Celery('order_service', broker=settings.broker_url,
             include=['tasks'])

if settings.test:
    SCHEDULE = timedelta(seconds=1)
else:
    SCHEDULE = timedelta(hours=12)

CELERYBEAT_SCHEDULE = {
    'handle_payment_orders': {
        'task': 'handle_payment_orders',
        'schedule': SCHEDULE,
        'options': {'queue': 'orders'},
        'args': tuple()
    },
}

app.conf.beat_schedule = CELERYBEAT_SCHEDULE
