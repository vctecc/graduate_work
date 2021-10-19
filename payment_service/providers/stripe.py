import stripe
import logging

from core.config import settings
from models.payment import PaymentState
from .base import BaseProvider
from .models import PaymentIntent


class Stripe(BaseProvider):
    base_api_url = ""

    def send_payment_request(self, provider_user_id: str, payment_amount: float, **kwargs) -> None:
        logging.info("Stripe got the payment request")
        return

    def acknowledge_payment_status(self, payment_id: str) -> PaymentState:

        provider_payment = stripe.PaymentIntent.retrieve(
            id=payment_id,
            api_key=settings.stripe_secret_key
        )
        payment = PaymentIntent(**provider_payment)

        logging.info(f"Stripe sent the payment {payment.id} status {payment.status}")
        return payment.status
