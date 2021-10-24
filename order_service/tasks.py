from celery import Task

from core.celery_app import app
from core.config import PAYMENTS_API_URL, SUBSCRIPTION_API_URL
from services.payment import PaymentService
from services.subscription import SubscriptionService

subscription_service = SubscriptionService(SUBSCRIPTION_API_URL)
payment_service = PaymentService(PAYMENTS_API_URL)


class BaseTaskWithRetry(Task): # noqa
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_payment_orders", acks_late=True, bind=True, base=BaseTaskWithRetry)
def handle_payment_orders(self):
    """Get unpaid subscriptions for the schedule period, register and send request to pay them"""

    pending_subscriptions = subscription_service.get_pending_subscriptions()

    for subscription in pending_subscriptions:
        payment_service.register_payment(subscription)
