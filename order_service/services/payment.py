import json
import logging
from urllib.parse import urljoin

import requests

from models.subscription import Subscription
from core.config import PaymentsSettings


class PaymentService:
    def __init__(self, settings: PaymentsSettings):
        self.settings = settings

    def register_payment(self, payment: Subscription):
        logging.info(f"Registering payment: {payment}")
        data = {
            "user_id": payment.user_id,
            "amount": str(payment.product.price),
            "product_id": payment.product.id,
            "currency": payment.product.currency_code
        }
        response = requests.post(urljoin(self.settings.url, 'v1/payments'),
                                 data=json.dumps(data))
        response.raise_for_status()
        logging.info("finished registering")
        return
