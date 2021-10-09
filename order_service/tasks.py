import logging

from .celery_app import app


@app.task(name="get_pending_subscriptions")
def get_pending_subscriptions():
    logging.info("Getting subscriptions")
