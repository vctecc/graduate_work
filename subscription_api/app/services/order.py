from datetime import datetime
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState

from .crud import CRUDBase


class OrderService(CRUDBase):
    async def get_subscriptions_for_payment(self, limit: int = 100) -> list:
        db_objs = self.db.query(self.model).filter(
            self.model.state == SubscriptionState.ACTIVE,
            self.model.end_date <= datetime.now()
        ).order_by(self.model.id).limit(limit).all()

        for dbo in db_objs:
            dbo.state = SubscriptionState.PRE_ACTIVATION
        self.db.commit()

        return db_objs


@lru_cache()
def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db, Subscription)
