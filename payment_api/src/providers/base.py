import abc

from src.providers.schemas import (ProviderPayment, ProviderPaymentCancel,
                                   ProviderPaymentResult)
from src.schemas.customer import CustomerSchema


class AbstractProvider(abc.ABC):

    @abc.abstractmethod
    async def create_customer(self) -> CustomerSchema:
        pass

    @abc.abstractmethod
    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        pass

    @abc.abstractmethod
    async def cancel(self, cancel: ProviderPaymentCancel):
        pass



