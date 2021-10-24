from pydantic import BaseModel

from .product import Product


class Subscription(BaseModel):
    order_id: str
    user_id: str
    subscription_id: str
    product: Product
