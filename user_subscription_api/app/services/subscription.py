import logging

from datetime import datetime, timedelta
from functools import lru_cache
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Any, Optional

from app.models.subscription import Subscription, SubscriptionState
from .crud import CRUDBase
from app.db.session import get_db


logger = logging.getLogger(__name__)


class SubscriptionService(CRUDBase):

    async def get_by_user_id(self, _id: Any):
        return self.db.query(self.model).filter(self.model.user_id == _id).first()

    async def change_state(self, _id: Any, state: str) -> Optional[Subscription]:
        db_obj = await self.get(_id)
        if not db_obj:
            return None

        db_obj.state = state
        self.db.commit()
        return db_obj

    async def cancel(self, _id: str) -> Optional[Subscription]:
        return await self.change_state(_id, SubscriptionState.CANCELLED)

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


# FIXME use async
@lru_cache()
def get_subscription_service(
        db: Session = Depends(get_db)) -> SubscriptionService:
    return SubscriptionService(db, Subscription)

