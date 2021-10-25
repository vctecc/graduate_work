import abc


class BaseProvider(abc.ABC):
    def send_payment_request(self, *args, **kwargs) -> None:
        pass

    def get_payment_status(self, *args, **kwargs) -> None:
        pass
