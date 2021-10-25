from pydantic import BaseModel

from .product import Product


class Subscription(BaseModel):
    id: str
    user_id: str
    product: Product
