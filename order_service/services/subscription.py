import logging
from typing import List
from urllib.parse import urljoin
import requests

from ..models.Subscription import Subscription


class SubscriptionService:
    def __init__(self, url):
        self.base_api_url = url

    def get_pending_subscriptions(self) -> List[Subscription]:
        response = requests.get(urljoin(self.base_api_url, 'subscriptions/'))
        response.raise_for_status()
        data = response.json()
        logging.info(f"Got subscriptions: {data}")
        return data
