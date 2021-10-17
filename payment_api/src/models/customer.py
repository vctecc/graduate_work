from sqlalchemy import Column, String
from src.models.base import AbstractModel


class Customer(AbstractModel):
    __tablename__ = "customers"

    user_id = Column(String)
    customer_id = Column(String)

