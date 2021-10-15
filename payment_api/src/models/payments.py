import enum
from sqlalchemy import Column, String, Enum
from src.models.base import AbstractModel


class PaymentState(enum.Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PAID = "paid"
    ERROR = "error"


class Payment(AbstractModel):
    __tablename__ = "payments"

    invoice_id = Column(String)
    customer_id = Column(String)
    status = Column(Enum(PaymentState))

