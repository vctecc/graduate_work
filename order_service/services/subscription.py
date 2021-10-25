import logging
from typing import Tuple
from urllib.parse import urljoin

import requests

from models.subscription import Subscription
from core.config import SubscriptionSettings


class SubscriptionService:
    def __init__(self, settings: SubscriptionSettings):
        self.settings = settings

    def get_pending_subscriptions(self) -> Tuple[Subscription]:
        response = requests.get(urljoin(self.settings.url, 'v1/service/orders'))
        response.raise_for_status()
        data = response.json()
        subscriptions = tuple(Subscription(**item) for item in data)
        logging.info(f"Got subscriptions: {subscriptions}")
        return subscriptions
