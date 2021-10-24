import logging
from datetime import datetime, timedelta
from functools import lru_cache

from typing import Any, ClassVar, Optional

from typing import Any, Optional
from uuid import UUID


from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

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

    async def create_subscription(self, obj: CreateSchemaType) -> Optional[Subscription]:
        product = self.db.execute(
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

        return await self.create(obj.dict())

    #  FIXME remove it
    async def get_user_subscription(self, user_id: UUID, product: Product) -> Subscription:

        user_subscription = self.db.execute(
            select(
                Subscription.id
            ).where(
                Subscription.user_id == user_id,
                Subscription.product == product
            )
        )
        user_subscription = user_subscription.first()
        return user_subscription

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
