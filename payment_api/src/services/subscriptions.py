import aiohttp

from src.core.config import SubscriptionsSettings, settings
from src.schemas.subscriptions import ProductSchema, SubscriptionSchema


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
    async def update_subscription(cls, subscription: SubscriptionSchema) -> None:
        session = aiohttp.ClientSession()
        url = f'{cls.settings.url}/service/subscription'
        body = subscription.dict()
        response = await session.post(url, json=body) # noqa
        await session.close()


class SubscriptionMock(object):

    @classmethod
    async def get_product(cls, product_id: str) -> ProductSchema:
        return ProductSchema(
            id='a49b436a-d0b3-4e3e-84e5-ac9204a330a5',
            name='the podpiska',
            price=10000
        )

    @classmethod
    async def update_subscription(cls, subscription: SubscriptionSchema) -> None:
        ...


def get_subscriptions_service():
    if settings.test:
        return SubscriptionMock()

    return SubscriptionService()
