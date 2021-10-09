from celery import Celery

from .config import BROKER_URL, CELERYBEAT_SCHEDULE


app = Celery('order_service', broker=BROKER_URL,
             include=['order_service.tasks'])
app.conf.beat_schedule = CELERYBEAT_SCHEDULE
