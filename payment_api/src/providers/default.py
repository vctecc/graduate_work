from src.providers.stripe import StripeProvider


def get_default_provider():
    return StripeProvider()
