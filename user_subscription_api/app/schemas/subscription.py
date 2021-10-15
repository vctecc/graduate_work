import datetime

from models.subscription import SubscriptionState
from pydantic import BaseModel

from .product import Product


class Subscription(BaseModel):
    product: Product
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState

    class Config:
        orm_mode = True
