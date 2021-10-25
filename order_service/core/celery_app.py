from datetime import timedelta

from celery import Celery

from .config import settings

app = Celery('order_service', broker=settings.broker_url,
             include=['tasks'])

SCHEDULE = timedelta(seconds=30)

CELERYBEAT_SCHEDULE = {
    'handle_payment_orders': {
        'task': 'handle_payment_orders',
        'schedule': SCHEDULE,
        'options': {'queue': 'orders'},
        'args': ()
    },
}

app.conf.beat_schedule = CELERYBEAT_SCHEDULE
