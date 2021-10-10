import logging
from datetime import timedelta
from typing import List
from urllib.parse import urljoin

import requests
from ..models.Subscription import Subscription


class SubscriptionService:
    def __init__(self, url):
        self.base_api_url = url

    def get_pending_subscriptions(self, period: timedelta) -> List[Subscription]:
        params = {
            "period_hrs": period.seconds/3600
        }
        response = requests.get(urljoin(self.base_api_url, 'subscriptions/'), params=params)
        response.raise_for_status()
        data = response.json()
        logging.info(f"Got subscriptions: {data}")
        return data


'''sub = SubscriptionService("https://31e9ff3d-42ad-467e-9eb6-ccfa680d9f00.mock.pstmn.io/api/v1/")
sub.get_pending_subscriptions(timedelta(seconds=30))'''