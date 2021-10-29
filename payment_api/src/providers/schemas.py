from src.schemas.base import AbstractSchema


class ProviderBase(AbstractSchema):
    amount: int
    customer: str
    currency: str = "RUB"


class ProviderPayment(ProviderBase):
    setup_future_usage: str = 'off_session'
    confirm: bool = False


class ProviderPaymentCancel(ProviderBase):
    payment: str


class ProviderPaymentResult(AbstractSchema):
    id: str
    client_secret: str

