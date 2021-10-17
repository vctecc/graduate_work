from src.models import PaymentState
from src.schemas import AbstractSchema


class PaymentSchema(AbstractSchema):
    id: str
    customer_id: str
    invoice_id: str
    status: PaymentState

    class Config:
        orm_mode = True
        use_enum_values = True


class NewPaymentSchema(AbstractSchema):
    product: str
    currency: str


class NewPaymentResult(AbstractSchema):
    id: str
    client_secret: str
