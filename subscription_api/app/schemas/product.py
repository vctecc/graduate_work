from decimal import Decimal
from app.schemas.base import BaseSchema


class Product(BaseSchema):
    price: Decimal
    currency_code: str
    period: int
    is_active: bool


class ProductDetail(BaseSchema):
    name: str
    description: str
    price: Decimal
    currency_code: str
    period: int
    is_active: bool
