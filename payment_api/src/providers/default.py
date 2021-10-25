from src.core.config import settings
from src.providers.stripe.provider import StripeProvider, StripeProviderMock


def get_default_provider():
    if settings.test:
        return StripeProviderMock()

    return StripeProvider()
