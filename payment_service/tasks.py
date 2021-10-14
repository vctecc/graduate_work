import traceback
from abc import ABC

from celery import Task

from core.celery_app import app
from core.config import PAYMENTS_API_URL
from services.payment import PaymentService
from providers.stripe import Stripe

payment_service = PaymentService(PAYMENTS_API_URL)
provider = Stripe()


class BaseTaskWithRetry(Task, ABC):
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_pending_payments", acks_late=True, bind=True, base=BaseTaskWithRetry)
def handle_pending_payments(self):
    """Get pending payments from DB, acknowledge their status and update payment in DB"""
    processing_payments = payment_service.get_processing_payments()

    for payment in processing_payments:
        status = provider.acknowledge_payment_status(payment["provider_user_id"])
        if status is not "Processing":
            payment_service.update_payment_status(payment["id"], status)

