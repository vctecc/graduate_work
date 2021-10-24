from typing import Optional

import stripe
from src.providers import AbstractProvider, ProviderPaymentResult, ProviderPayment
from src.providers.schemas import ProviderPaymentCancel
from src.schemas.customer import CustomerSchema


class StripeProvider(AbstractProvider):

    async def create_customer(self) -> CustomerSchema:
        stripe_customer = stripe.Customer.create()
        return CustomerSchema(id=stripe_customer['id'])

    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        payment_method = await self.customer_payment_method(payment.customer)

        payment_intent = stripe.PaymentIntent.create(
            **payment.dict(),
            payment_method=payment_method,
        )
        return ProviderPaymentResult(
            id=payment_intent['id'],
            client_secret=payment_intent['client_secret'],
        )

    async def cancel(self, cancel: ProviderPaymentCancel):
        return stripe.Refund.create(
            amount=cancel.amount,
            payment_intent=cancel.payment,
        )

    @classmethod
    async def customer_payment_method(cls, customer: str) -> Optional[str]:
        methods = stripe.PaymentMethod.list(
            customer=customer,
            type='card'
        )

        if not methods:
            return None

        return methods['data'][0]['id']


class StripeProviderMock(AbstractProvider):

    async def create_customer(self) -> CustomerSchema:
        return CustomerSchema(id='cus_KSkOhnNYigh8Mc')

    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        return ProviderPaymentResult(
            id='pi_3JnrIvEZwW9AoJC20hPPg3ua',
            client_secret='big_secret',
        )

    async def cancel(self, cancel: ProviderPaymentCancel):
        ...
