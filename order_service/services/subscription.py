import logging
from typing import Tuple
from urllib.parse import urljoin
import requests

from models.subscription import Subscription


class SubscriptionService:
    def __init__(self, url):
        self.base_api_url = url

    def get_pending_subscriptions(self) -> Tuple[Subscription]:
        response = requests.get(urljoin(self.base_api_url, 'subscriptions/'))
        response.raise_for_status()
        data = response.json()
        logging.info(f"Got subscriptions: {data}")
        subscriptions = tuple(Subscription(**item) for item in data)
        return subscriptions

