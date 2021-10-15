import datetime
from uuid import UUID

from pydantic import BaseModel

from app.models.subscription import SubscriptionState

from .product import Product


class SubscriptionDetails(BaseModel):
    user_id: UUID
    product: Product
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState

    class Config:
        orm_mode = True


class SubscriptionPreview(BaseModel):
    product_id: UUID
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState

    class Config:
        orm_mode = True
