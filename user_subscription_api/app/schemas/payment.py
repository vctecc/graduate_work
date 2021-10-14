"""Module with API schemas"""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel
from enum import Enum


class PaymentSystem(str, Enum):
    STRIPE = "stripe"


class PaymentInfoIn(BaseModel):
    product_id: str
    email: str
    payment_system: PaymentSystem
