import logging
from abc import ABC
from celery import Task

from core.celery_app import app
from core.config import settings
from services.payment import PaymentService
from providers.stripe import Stripe, StripeMock

payment_service = PaymentService(settings.payments_api)

if settings.test:
    provider = StripeMock()
else:
    provider = Stripe()


class BaseTaskWithRetry(Task): # noqa
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_pending_payments", acks_late=True)
def handle_pending_payments():
    """Get pending payments from DB, acknowledge their status and update payment in DB"""
    for payment in payment_service.processing_payments():
        payment.status = provider.get_payment_status(payment.invoice_id)
        payment_service.update_status(payment)

