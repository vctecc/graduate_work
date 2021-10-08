from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class PaymentState(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PAID = "paid"
    ERROR = "error"


class Payment(BaseModel):
    id: str
    user_id: str
    state: PaymentState
    is_automatic: bool
    is_refund: bool
