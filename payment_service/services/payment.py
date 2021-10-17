import logging
from typing import List

import requests

from models.payment import Payment, PaymentState

from core.config import PaymentsSettings


class PaymentService:
    def __init__(self, settings: PaymentsSettings):
        self.settings = settings

    def processing_payments(self) -> List[Payment]:
        url = f'{self.settings.url}/payments/processing'
        logging.info(url)
        response = requests.get(url)
        data = response.json()
        processing_payments = [Payment(**item) for item in data]
        logging.info(f"Got processing payments: {processing_payments}")
        return processing_payments

    def update_payment_status(self, payment_id, payment_status):
        logging.info(f"Updated payment status for {payment_id} to {payment_status}")
