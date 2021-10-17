import enum

from pydantic import BaseModel


class PaymentState(enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PAID = "paid"
    CANCELED = "canceled"
    ERROR = "error"


class Payment(BaseModel):
    id: str
    provider_customer_id: str
    invoice_id: str
    product_id: str
    user_id: str
    status: PaymentState

    class Config:
        use_enum_values = True
