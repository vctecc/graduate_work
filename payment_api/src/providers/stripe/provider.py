import stripe
from src.core.config import STRIPE_SECRET_KEY
from src.providers import AbstractProvider, ProviderPaymentResult, ProviderPayment
from src.schemas import CustomerSchema


class StripeProvider(AbstractProvider):

    async def create_customer(self) -> CustomerSchema:
        stripe_customer = stripe.Customer.create(api_key=STRIPE_SECRET_KEY)
        return CustomerSchema(id=stripe_customer["id"])

    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        payment_intent = stripe.PaymentIntent.create(api_key=STRIPE_SECRET_KEY, **payment.dict())
        return ProviderPaymentResult(
            id=payment_intent["id"],
            client_secret=payment_intent["client_secret"],
        )
