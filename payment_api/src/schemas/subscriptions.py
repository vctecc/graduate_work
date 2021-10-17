from src.schemas import AbstractSchema


class ProductSchema(AbstractSchema):
    id: str
    name: str
    price: int


class SubscriptionSchema(AbstractSchema):
    user_id: str
    product: int
