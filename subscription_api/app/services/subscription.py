import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState
from app.schemas import Product

from .crud import CRUDBase

logger = logging.getLogger(__name__)


class SubscriptionService(CRUDBase):

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
        db: Session = Depends(get_db),
) -> SubscriptionService:
    return SubscriptionService(db, Subscription)
