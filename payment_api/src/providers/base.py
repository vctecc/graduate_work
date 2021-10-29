import abc

from src.providers.schemas import (
    ProviderPayment, ProviderPaymentCancel, ProviderPaymentResult,
)
from src.schemas.customer import CustomerSchema


class AbstractProvider(abc.ABC):

    @abc.abstractmethod
    async def create_customer(self) -> CustomerSchema:
        ...  # noqa: WPS428

    @abc.abstractmethod
    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        ...  # noqa: WPS428

    @abc.abstractmethod
    async def cancel(self, cancel: ProviderPaymentCancel):
        ...  # noqa: WPS428


def get_default_provider():
    from src.providers.stripe.provider import StripeProvider
    return StripeProvider()
