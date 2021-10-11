import logging
from urllib.parse import urljoin

import requests

from models.PaidFacility import PaidFacility


class PaymentService:
    def __init__(self, url):
        self.base_api_url = url

    def register_payment(self, payment: PaidFacility):
        logging.info(f"Registering payment: {payment}")
        response = requests.post(urljoin(self.base_api_url, 'payment/'), data=payment)
        response.raise_for_status()
        logging.info("finished registering")
        return
