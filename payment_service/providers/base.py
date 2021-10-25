import abc

from models.payment import PaymentState


class BaseProvider(abc.ABC):

    @abc.abstractmethod
    def get_payment_status(self, *args, **kwargs) -> PaymentState:
        pass
