from src.schemas import AbstractSchema


class ProductSchema(AbstractSchema):
    id: str
    name: str
    price: int

