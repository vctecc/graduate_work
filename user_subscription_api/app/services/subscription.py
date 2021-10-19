import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Optional, ClassVar

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState
from app.models.product import Product
from app.core.exceptions import ProductNotFound
from app.schemas.base import CreateSchemaType

from .crud import CRUDBase

logger = logging.getLogger(__name__)


class SubscriptionService(CRUDBase):

    def __init__(self, db: Session, model: ClassVar, product_model: ClassVar):
        super().__init__(db, model)
        self.product_model = product_model

    async def create_subscription(self, obj: CreateSchemaType) -> Optional[Subscription]:
        p_obj = self.db.query(self.product_model).filter(
            self.product_model.id == obj.product_id).first()

        if not p_obj:
            raise ProductNotFound

        if not obj.end_date:
            obj.end_date = obj.start_date + timedelta(days=p_obj.period)

        return await self.create(obj.dict())

    async def change_state(self, _id: Any, state: str) -> Optional[Subscription]:
        db_obj = await self.get(_id)
        if not db_obj:
            return None

        db_obj.state = state
        self.db.commit()
        return db_obj

    async def deactivate(self, _id: str) -> Optional[Subscription]:
        return await self.change_state(_id, SubscriptionState.INACTIVE)

    async def activate(self, _id: str,
                       period: Optional[int] = None) -> Optional[Subscription]:
        db_obj = await self.get(_id)
        if not db_obj:
            return None

        if not period:
            period = db_obj.product.period

        now = datetime.now()
        update_data = {
            "state": SubscriptionState.ACTIVE,
            "start_date": now,
            "end_date": now + timedelta(days=period)
        }

        return await self.update(db_obj, update_data)


@lru_cache()
def get_subscription_service(
        db: Session = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(db, Subscription, Product)
