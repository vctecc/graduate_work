from abc import ABC

from celery import Task

from core.celery_app import app
from core.config import SUBSCRIPTION_API_URL, PAYMENTS_API_URL
from services.subscription import SubscriptionService
from services.payment import PaymentService
from providers.stripe import Stripe


subscription_service = SubscriptionService(SUBSCRIPTION_API_URL)
payment_service = PaymentService(PAYMENTS_API_URL)
provider = Stripe()


class BaseTaskWithRetry(Task, ABC):
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_payment_orders", acks_late=True, bind=True, base=BaseTaskWithRetry)
def handle_payment_orders(self):
    """Get unpaid subscriptions for the schedule period, register and pay them"""

    pending_subscriptions = subscription_service.get_pending_subscriptions()

    for subscription in pending_subscriptions:
        payment_service.register_payment(subscription)
        provider.send_payment_request(subscription.provider_user_id, subscription.payment_amount)

