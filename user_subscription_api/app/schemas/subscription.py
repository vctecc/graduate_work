import datetime
from pydantic import BaseModel

from .product import Product
from models import SubscriptionState


class Subscription(BaseModel):
    product: Product
    start_date: datetime.date
    end_date: datetime.date
    state: SubscriptionState
