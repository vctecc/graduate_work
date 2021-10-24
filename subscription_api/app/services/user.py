import logging
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Optional

from fastapi import Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.db.session import get_db
from app.models.subscription import Subscription, SubscriptionState
from app.models.product import Product
from app.schemas import SubscriptionDetails
from app.schemas.subscription import SubscriptionShort
from . import ProductService, get_product_service

from .crud import CRUDBase
from .subscription import SubscriptionService, get_subscription_service

logger = logging.getLogger(__name__)


class UserService(CRUDBase):

    def __init__(
            self,
            db: Session,
            model,
            product_service: ProductService,
            subscription_service: SubscriptionService,
    ):
        super(UserService, self).__init__(db, model)
        self.product_service = product_service
        self.subscription_service = subscription_service

    async def set_user_subscription(self, subscription: SubscriptionShort):

        product = await self.product_service.get(subscription.product_id)
        user_subscription = await self.subscription_service.get_user_subscription(
            subscription.user_id, subscription.id)

        if not user_subscription:
            subscription = SubscriptionDetails(
                user_id=subscription.user_id,
                product_id=product.id,
                state=SubscriptionState.ACTIVE,
                start_date=datetime.now(),
                end_date=datetime.now() + timedelta(days=product.period)
            )
            await self.subscription_service.create(subscription.dict())
        else:
            await self.subscription_service.activate(user_subscription.id, product.period)

    async def get_user_subscription(self, user_id: Any, subscription_id: Any):
        obj = await self.db.execute(
            select(
                self.model
            ).options(
                selectinload(self.model.product)
            ).where(
                self.model.user_id == user_id,
                self.model.id == subscription_id
            )
        )
        return obj.scalar_one_or_none()

    async def get_all_user_subscriptions(self, user_id: Any):
        obj = await self.db.execute(
            select(
                self.model
            ).options(
                selectinload(self.model.product)
            ).where(
                self.model.user_id == user_id,
            )
        )
        return obj.scalars().all()

    async def cancel(self, user_id: Any, subscription_id: Any):
        db_obj = await self.get_user_subscription(user_id, subscription_id)
        if not db_obj:
            return None

        db_obj.state = SubscriptionState.CANCELLED
        await self.db.commit()
        return db_obj

    async def refund(self, user_id: Any, subscription_id: Any):
        pass


@lru_cache()
def get_user_service(
        db: Session = Depends(get_db),
        product_service: ProductService = Depends(get_product_service),
        subscription_service: SubscriptionService = Depends(get_subscription_service),

) -> UserService:
    return UserService(
        db,
        Subscription,
        product_service,
        subscription_service,
    )

