import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState
from models.product import Product

from schemas import SubscriptionDetails
from . import get_product_service, ProductService

from .crud import CRUDBase

logger = logging.getLogger(__name__)


class SubscriptionService(CRUDBase):

    def __init__(self, db: Session, model, product_service: ProductService):
        super(SubscriptionService, self).__init__(db, model)
        self.product_service = product_service

    async def set_user_subscription(self, user_id: str, product_id: str):

        product: Product = await self.product_service.get(product_id)

        user_subscription = await self.db.execute(
            select(
                Subscription
            ).where(
                Subscription.user_id == user_id,
                Subscription.product == product_id
            ).first()
        )

        if not user_subscription:
            subscription = SubscriptionDetails(
                user_id=user_id,
                product_id=product.id,
                state=SubscriptionState.ACTIVE,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=product.period)
            )
            await self.create(subscription.dict())
        else:
            await self.activate(user_subscription.id, product.period)

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


# FIXME use async
@lru_cache()
def get_subscription_service(
        db: Session = Depends(get_db),
        product_service: ProductService = Depends(get_product_service),
) -> SubscriptionService:
    return SubscriptionService(db, Subscription, product_service)
