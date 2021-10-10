import logging

from .base import BaseProvider


class Stripe(BaseProvider):
    base_api_url = ""

    def send_payment_request(self, provider_user_id: str, payment_amount: float, **kwargs) -> None:
        logging.info("Stripe got the payment request")
        return
