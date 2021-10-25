from celery import Task

from core.celery_app import app
from core.config import settings
from services.payment import PaymentService
from services.subscription import SubscriptionService
from models.subscription import Subscription

subscription_service = SubscriptionService(settings.subscription_api)
payment_service = PaymentService(settings.payments_api)


class BaseTaskWithRetry(Task): # noqa
    """ Handle connection errors."""
    autoretry_for = (ConnectionError,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True


@app.task(name="handle_payment_orders", acks_late=True,
          bind=True, base=BaseTaskWithRetry)
def handle_payment_orders(self):
    """Get unpaid subscriptions for the schedule period,
     register and send request to pay them"""
    pending_subscriptions = subscription_service.get_pending_subscriptions()

    for subscription in pending_subscriptions:
        register_payment.apply_async(args=[subscription.dict()],
                                     queue='registrations',
                                     routing_key='keys.register')


@app.task(name="register_payment", acks_late=True, bind=True, base=BaseTaskWithRetry)
def register_payment(self, subscription):
    subscription_obj = Subscription(**subscription)
    payment_service.register_payment(subscription_obj)
