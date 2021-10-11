from sqlalchemy import Column, String
from src.models.base import AbstractModel


class Customer(AbstractModel):
    __tablename__ = "customers"

    provider_id = Column(String)
    user_id = Column(String)
