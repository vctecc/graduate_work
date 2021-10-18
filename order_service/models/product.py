from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    description: str
    period: int
    price: int
    currency_code: str
    is_active: bool
    subscriptions: list