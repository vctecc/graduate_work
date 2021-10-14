from abc import ABC

from celery import Task

from core.celery_app import app
from core.config import SUBSCRIPTION_API_URL, PAYMENTS_API_URL


class BaseTaskWithRetry(Task, ABC):
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_pending_payments", acks_late=True, bind=True, base=BaseTaskWithRetry)
def handle_pending_payments(self):
    """Get pending payments from DB, acknowledge their status and update payment in DB"""

    print("handle pending payment")

