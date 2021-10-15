import abc

from src.providers.schemas import ProviderPayment, ProviderPaymentResult
from src.schemas import CustomerSchema


class AbstractProvider(abc.ABC):

    @abc.abstractmethod
    async def create_customer(self) -> CustomerSchema:
        pass

    @abc.abstractmethod
    async def create_payment(self, payment: ProviderPayment) -> ProviderPaymentResult:
        pass


