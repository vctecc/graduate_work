from functools import lru_cache


class UserSubscriptionService:
    def __init__(self):
        pass

    async def get(self, _id: str):
        pass

    async def cancel(self, _id: str):
        pass


# FIXME use async
@lru_cache()
def get_user_subscription_service(
) -> UserSubscriptionService:
    return UserSubscriptionService()
