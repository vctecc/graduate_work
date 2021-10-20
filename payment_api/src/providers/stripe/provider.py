import stripe
from src.providers import AbstractProvider, ProviderPaymentResult, ProviderPayment
from src.providers.schemas import ProviderPaymentCancel
from src.schemas.customer import CustomerSchema


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

    async def cancel(self, cancel: ProviderPaymentCancel):

        return stripe.Refund.create(
            amount=cancel.amount,
            payment_intent=cancel.payment,
        )

    async def customer_payment_method(self, customer: str) -> str:
        methods = stripe.PaymentMethod.list(
            customer=customer,
            type='card'
        )

        if not methods:
            raise Exception('No payment method.')

        return methods['data'][0]['id']

