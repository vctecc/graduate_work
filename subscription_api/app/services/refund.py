import logging
from functools import lru_cache

import aiohttp
from aiohttp import client_exceptions

from app.core.config import PaymentsAPISettings, settings
from app.core.exceptions import PaymentAPIUnavailable
from app.models.subscription import Subscription
from app.schemas.order import OrderRefund

logger = logging.getLogger(__name__)


class RefundService:
    settings: PaymentsAPISettings = PaymentsAPISettings()

    @classmethod
    def _convert(cls, subscription: Subscription):
        return OrderRefund(
            user_id=subscription.user_id,
            amount=subscription.product.price,
            currency=subscription.product.currency_code
        )

    async def refund(self, subscription: Subscription):
        order = self._convert(subscription)
        async with aiohttp.ClientSession() as session:
            try:
                await session.post(self.settings.url, json=order.json())
            except client_exceptions.ClientConnectorError:
                raise PaymentAPIUnavailable


class RefundServiceMock(RefundService):
    async def refund(self, subscription: Subscription):
        order = self._convert(subscription)
        logger.info(order.json())


@lru_cache()
def get_refund_service():
    if settings.debug:
        return RefundServiceMock()
    return RefundService()
