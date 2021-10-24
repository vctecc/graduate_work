import enum
from sqlalchemy import Column, String, Enum, ForeignKey
from src.models.base import AbstractModel


class PaymentState(str, enum.Enum):
    DRAFT = "draft"
    PRE_PROCESSING = "pre_processing"
    PROCESSING = "processing"
    PAID = "paid"
    ERROR = "error"
    CANCELED = "canceled"


class Payment(AbstractModel):
    __tablename__ = "payments"

    invoice_id = Column(String)
    product_id = Column(String)
    customer_id = Column(ForeignKey("customers.id"))
    status = Column(Enum(PaymentState))

