import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState

from .crud import CRUDBase

logger = logging.getLogger(__name__)


class UserService(CRUDBase):

    async def get_user_subscription(self, user_id: Any, subscription_id: Any):
        return self.db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.id == subscription_id).first()

    async def get_all_user_subscriptions(self, user_id: Any):
        return self.db.query(self.model).filter(
            self.model.user_id == user_id).all()

    async def cancel(self, user_id: Any, subscription_id: Any):
        db_obj = await self.get_user_subscription(user_id, subscription_id)
        if not db_obj:
            return None

        db_obj.state = SubscriptionState.CANCELLED
        self.db.commit()
        return db_obj

    async def refund(self, user_id: Any, subscription_id: Any):
        pass


# FIXME use async
@lru_cache()
def get_user_service(
        db: Session = Depends(get_db)) -> UserService:
    return UserService(db, Subscription)

