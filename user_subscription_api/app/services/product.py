from typing import ClassVar
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import Depends

from app.models.product import Product
from app.db.session import get_db
from .crud import CRUDBase


class ProductService(CRUDBase):
    async def get_all(self, skip: int = 0, limit: int = 100,
                      only_active: bool = False) -> list:

        query = self.db.query(self.model)

        if only_active:
            query = query.filter(self.model.is_active == True)  # noqa

        return query.offset(skip).limit(limit).all()


# FIXME use async
@lru_cache()
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(db, Product)
