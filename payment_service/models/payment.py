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
    customer_id: str
    invoice_id: str
    status: str
