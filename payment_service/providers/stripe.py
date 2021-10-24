import stripe
import logging

from core.config import settings
from models.payment import PaymentState
from .base import BaseProvider
from .models import PaymentIntent


class Stripe(BaseProvider):

    @classmethod
    def get_payment_status(cls, payment_id: str) -> PaymentState:
        provider_payment = stripe.PaymentIntent.retrieve(
            id=payment_id,
            api_key=settings.stripe_secret_key
        )
        payment = PaymentIntent(**provider_payment)

        logging.info(f"Stripe sent the payment {payment.id} status {payment.status}")
        return payment.status


class StripeMock(BaseProvider):

    @classmethod
    def get_payment_status(cls, payment_id: str) -> PaymentState:
        return PaymentState.PAID
