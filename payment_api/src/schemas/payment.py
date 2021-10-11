from src.schemas.base import AbstractSchema


class PaymentSchema(AbstractSchema):
    customer_id: str
    provider_id: str
    status: str

    class Config:
        orm_mode = True


class NewPaymentSchema(AbstractSchema):
    product: str
    currency: str
    price: int
    quantity: int = 1

