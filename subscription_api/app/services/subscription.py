import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, ClassVar, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import ProductNotFound
from app.db.session import get_db
from app.models.product import Product
from app.models.subscription import Subscription, SubscriptionState
from app.schemas.base import CreateSchemaType
from .crud import CRUDBase

logger = logging.getLogger(__name__)


class SubscriptionService(CRUDBase):

    def __init__(self, db: Session, model: ClassVar, product_model: ClassVar):
        super().__init__(db, model)
        self.product_model = product_model

    async def get(self, _id: Any):
        stmt = select(
            self.model
        ).where(
            self.model.id == _id
        ).options(
            selectinload(self.model.product)
        )
        obj = await self.db.execute(stmt)
        return obj.scalar_one_or_none()

    async def create(self, obj: dict):
        db_obj = self.model(**obj)
        self.db.add(db_obj)
        await self.db.commit()
        return await self.get(db_obj.id)

    async def create_subscription(self, obj: CreateSchemaType) -> Optional[Subscription]:
        product = await self.db.execute(
            select(
                self.product_model
            ).where(
                self.product_model.id == obj.product_id
            )
        )
        product = product.scalar_one_or_none()
        if not product:
            raise ProductNotFound

        if not obj.end_date:
            obj.end_date = obj.start_date + timedelta(days=product.period)

        subscription = await self.db.execute(
            select(
                self.model
            ).where(
                self.model.user_id == obj.user_id,
                self.model.product_id == obj.product_id
            ).options(
                selectinload(self.model.product)
            )
        )

        subscription = subscription.scalar_one_or_none()
        if subscription:
            subscription.end_date = obj.end_date
            subscription.state = SubscriptionState.ACTIVE
            await self.db.commit()
            return subscription

        return await self.create(obj.dict())

    async def change_state(self, _id: Any, state: str) -> Optional[Subscription]:
        db_obj = await self.get(_id)
        if not db_obj:
            return None

        db_obj.state = state
        await self.db.commit()
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
