from enum import Enum
from src.schemas.base import AbstractSchema


class PaymentState(str, Enum):
    DRAFT = "draft"
    PROCESSING = "processing"
    PAID = "paid"
    ERROR = "error"


class Payment(AbstractSchema):
    id: str
    user_id: str
    state: PaymentState
    is_automatic: bool
    is_refund: bool


class CustomerSchema(AbstractSchema):
    id: str
    provider_id: str
    user_id: str

    class Config:
        orm_mode = True


class Subscription(AbstractSchema):
    id: str
    user_id: str
