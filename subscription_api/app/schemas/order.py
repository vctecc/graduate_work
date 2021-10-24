from uuid import UUID

from pydantic import Field

from app.schemas.base import FastModel
from app.schemas.product import Product


class Order(FastModel):
    user_id: UUID
    subscription_id: UUID = Field(alias='id')
    product: Product
