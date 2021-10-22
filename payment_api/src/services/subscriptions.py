import aiohttp

from src.schemas.subscriptions import ProductSchema, SubscriptionSchema
from src.core.config import settings, SubscriptionsSettings


class SubscriptionService(object):
    settings: SubscriptionsSettings = settings.subscriptions

    @classmethod
    async def get_product(cls, product_id: str) -> ProductSchema:
        session = aiohttp.ClientSession()
        async with session.get(f'{cls.settings.url}/product/{product_id}') as response:
            body = await response.json()
            product = ProductSchema(**body)
        await session.close()
        return product

    @classmethod
    async def add_subscription(cls, subscription: SubscriptionSchema) -> None:
        session = aiohttp.ClientSession()
        url = f'{cls.settings.url}/subscription'
        body = subscription.dict()
        await session.post(url, json=body)
        await session.close()


def get_subscriptions_service():
    return SubscriptionService()
