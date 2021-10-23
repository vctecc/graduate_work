from src.providers.stripe.provider import StripeProvider, StripeProviderMock
from src.core.config import settings


def get_default_provider():
    if settings.test:
        return StripeProviderMock()

    return StripeProvider()
