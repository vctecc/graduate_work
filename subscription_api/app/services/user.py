import logging
from functools import lru_cache
from typing import Any
from uuid import UUID

from aioredis import Redis
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.session import get_db
from app.db.cache import get_cache
from app.models.subscription import Subscription, SubscriptionState
from . import ProductService, get_product_service
from .crud import CRUDBase
from .subscription import SubscriptionService, get_subscription_service

logger = logging.getLogger(__name__)


class UserService(CRUDBase):

    def __init__(
            self,
            db: Session,
            cache: Redis,
            model,
            product_service: ProductService,
            subscription_service: SubscriptionService,
    ):
        super(UserService, self).__init__(db, model)
        self.cache = cache
        self.product_service = product_service
        self.subscription_service = subscription_service

    async def check_access(self, user_id: UUID, product_id: UUID) -> bool:
        key = f'{user_id}.{product_id}'

        check = await self.cache.get(key)
        if check:
            logger.debug('get user access from cache')
            return True

        check = await self.db.execute(
            select(self.model.id).where(
                self.model.user_id == user_id,
                self.model.product_id == product_id,
            )
        )

        if not check.first():
            return False

        await self.cache.set(key, 1)
        logger.debug('set user access to cache')
        return True

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
        cache: Redis = Depends(get_cache),
        product_service: ProductService = Depends(get_product_service),
        subscription_service: SubscriptionService = Depends(get_subscription_service),
) -> UserService:
    return UserService(
        db,
        cache,
        Subscription,
        product_service,
        subscription_service,
    )

