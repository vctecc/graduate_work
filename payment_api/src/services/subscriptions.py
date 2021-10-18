import aiohttp

from src.schemas.subscriptions import ProductSchema
from src.core.config import settings, SubscriptionsSettings


class SubscriptionService(object):

    settings: SubscriptionsSettings

    def __init__(self, settings: SubscriptionsSettings):
        self.settings = settings

    @classmethod
    async def get_product(cls, product_id: str) -> ProductSchema:
        async with aiohttp.ClientSession().get(f'{cls.settings.url}/product/{product_id}') as response:
            body = await response.json()
            return ProductSchema(**body)

    @classmethod
    async def add_subscription(cls, user_id: str, product_id: str) -> None:
        async with aiohttp.ClientSession().post(f'{cls.settings.url}/subscription') as response:
            return None

def get_subscriptions_service():
    return SubscriptionService(settings.subscriptions)

