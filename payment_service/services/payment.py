import logging
from urllib.parse import urljoin

import requests

from models.payment import Payment


class PaymentService:
    def __init__(self, url):
        self.base_api_url = url

    def get_processing_payments(self) -> list[Payment]:
        url = urljoin(self.base_api_url, 'payment/')
        response = requests.get(url, params={"status": "Processing"})
        response.raise_for_status()
        processing_payments = response.json()
        logging.info(f"Got processing payments: {processing_payments}")
        return processing_payments

    def update_payment_status(self, payment_id, payment_status):
        logging.info(f"Updated payment status for {payment_id} to {payment_status}")
