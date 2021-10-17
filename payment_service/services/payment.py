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

    def update_status(self, payment_id: str, status: PaymentState):
        if status == PaymentState.PROCESSING:
            return

        url = f'{self.settings.url}/payments/{payment_id}/status'
        requests.patch(url, params={'status': status.value})
        logging.info(f"Updated payment status for {payment_id} to {status.value}")
