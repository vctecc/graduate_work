from functools import lru_cache


class ProductService:
    def __init__(self):
        pass

    async def find(self, _id: str):
        pass

    async def find_all(self, only_active=False) -> list:
        return []


# FIXME use async
@lru_cache()
def get_product_service(
) -> ProductService:
    return ProductService()
