from typing import Optional

from src.schemas import CustomerSchema


class SubscriptionService(object):

    @staticmethod
    async def get_customer(self, user_id) -> Optional[CustomerSchema]:
        return None

    @staticmethod
    async def get_product_price(self, product_id: str) -> int:
        return 100000

    @staticmethod
    async def add_subscription(self, user_id:str, product_id: str) -> None:
        pass


def get_subscriptions_service():
    return SubscriptionService()

