import stripe
from src.core.config import settings
from src.providers import AbstractProvider, ProviderPaymentResult, ProviderPayment
from src.schemas import CustomerSchema


class StripeProvider(AbstractProvider):

    async def create_customer(self) -> CustomerSchema:
        stripe_customer = stripe.Customer.create(api_key=settings.stripe_secret_key)
        return CustomerSchema(id=stripe_customer["id"])

    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        payment_intent = stripe.PaymentIntent.create(api_key=settings.stripe_secret_key, **payment.dict())
        return ProviderPaymentResult(
            id=payment_intent["id"],
            client_secret=payment_intent["client_secret"],
        )
