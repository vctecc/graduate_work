"""Module with API schemas"""

from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class PaymentSystem(str, Enum):
    STRIPE = "stripe"


class PaymentInfoIn(BaseModel):
    product_id: str
    email: str
    payment_system: PaymentSystem
