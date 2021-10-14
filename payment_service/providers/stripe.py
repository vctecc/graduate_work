import logging
import random

from .base import BaseProvider


class Stripe(BaseProvider):
    base_api_url = ""

    def send_payment_request(self, provider_user_id: str, payment_amount: float, **kwargs) -> None:
        logging.info("Stripe got the payment request")
        return

    def acknowledge_payment_status(self, provider_user_id: str, **kwargs) -> str:
        statuses = ["success", "failed", "Processing"]
        status = random.choice(statuses)
        logging.info(f"Stripe sent the payment status {status}")
        return status