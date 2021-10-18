import logging
from urllib.parse import urljoin

import requests

from models.subscription import Subscription


class PaymentService:
    def __init__(self, url):
        self.base_api_url = url

    def register_payment(self, payment: Subscription):
        logging.info(f"Registering payment: {payment}")
        data = {"user_id": payment.user_id, "price": payment.product.price}
        response = requests.post(urljoin(self.base_api_url, 'payments/register'), data=data)
        response.raise_for_status()
        logging.info("finished registering")
        return
