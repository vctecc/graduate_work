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

    def update_status(self, payment: Payment):
        if payment.status == PaymentState.PROCESSING:
            return

        logging.info(f"Updating payment {payment.dict()}")
        url = f'{self.settings.url}/payments/update_status'
        requests.patch(url, json=payment.dict())
        logging.info(f"Updated payment status for {payment.id} to {payment.status}")
