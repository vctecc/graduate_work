from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    id: UUID
    price: Decimal
    currency_code: str
    period: int
    is_active: bool

    class Config:
        orm_mode = True


class ProductDetail(BaseModel):
    id: UUID
    name: str
    description: str
    price: Decimal
    currency_code: str
    period: int
    is_active: bool

    class Config:
        orm_mode = True

