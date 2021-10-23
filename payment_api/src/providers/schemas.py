from src.schemas.base import AbstractSchema


class ProviderPayment(AbstractSchema):
    amount: int
    customer: str
    currency: str = "RUB"
    setup_future_usage: str = 'off_session'
    confirm = False


class ProviderPaymentResult(AbstractSchema):
    id: str
    client_secret: str


class ProviderPaymentCancel(AbstractSchema):
    customer: str
    amount: int
    payment: str
    currency: str = "RUB"
