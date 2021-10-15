from celery import Celery

from core.config import BROKER_URL, CELERYBEAT_SCHEDULE


app = Celery('payment_service', broker=BROKER_URL,
             include=['tasks'])
app.conf.beat_schedule = CELERYBEAT_SCHEDULE
