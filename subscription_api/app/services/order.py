from datetime import datetime
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState
from .crud import CRUDBase


class OrderService(CRUDBase):
    async def get_subscriptions_for_payment(self, limit: int = 100) -> list:
        objs = await self.db.execute(
            select(
                self.model
            ).options(
                selectinload(self.model.product)
            ).where(
                self.model.state == SubscriptionState.ACTIVE,
                self.model.end_date <= datetime.now()
            ).order_by(
                self.model.id
            ).limit(limit).with_for_update()
        )

        objs = objs.scalars().all()
        for dbo in objs:
            dbo.state = SubscriptionState.PRE_ACTIVATION

        await self.db.commit()
        return objs


@lru_cache()
def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(db, Subscription)
