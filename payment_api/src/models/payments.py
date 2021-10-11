from enum import Enum
from sqlalchemy import Column, String, Integer, ForeignKey
from src.models.base import AbstractModel


class PaymentState(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PAID = "paid"
    ERROR = "error"

class Customer(AbstractModel):
    __tablename__ = "customers"

    provider_id = Column(String)
    user_id = Column(String)


class Product(AbstractModel):
    __tablename__ = "products"

    name = Column(String)
    price = Column(Integer)


class Payment(AbstractModel):
    __tablename__ = "payments"

    customer_id = Column(ForeignKey('customers.id'))
    provider_id = Column(String)
    status = Column(String, Enum(PaymentState))
