import datetime
from uuid import UUID

from app.schemas.base import BaseSchema
from app.schemas.product import Product
from app.models.subscription import SubscriptionState


class SubscriptionShort(BaseSchema):
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
