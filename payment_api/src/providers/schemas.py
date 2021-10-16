from src.schemas.base import AbstractSchema


class ProviderPayment(AbstractSchema):
    amount: int
    currency: str = "RUB"
    customer: str


class ProviderPaymentResult(AbstractSchema):
    id: str
    client_secret: str
