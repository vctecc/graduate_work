import datetime
from typing import Optional
from uuid import UUID

from app.models.subscription import SubscriptionState
from app.schemas.base import BaseModel, BaseSchema
from app.schemas.product import Product


class SubscriptionShort(BaseModel):
    user_id: UUID
    product_id: UUID


class SubscriptionDetails(BaseSchema):
    user_id: UUID
    product: Product
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState


class SubscriptionPreview(BaseSchema):
    product_id: UUID
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState


class SubscriptionCreate(BaseModel):
    user_id: UUID
    product_id: UUID
    start_date: Optional[datetime.date] = datetime.date.today()
    end_date: Optional[datetime.date] = None
