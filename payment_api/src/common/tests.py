from unittest.mock import patch

from src.schemas.subscriptions import ProductSchema


def patch_services():
    patch_subscription()


def patch_subscription():
    product = ProductSchema(
        id='a49b436a-d0b3-4e3e-84e5-ac9204a330a5',
        name='the podpiska',
        price=10000,
    )
    patch(
        'src.services.subscriptions.SubscriptionService.get_product',
        return_value=product,
    )

    patch(
        'src.services.subscriptions.SubscriptionService.update_subscription',
        return_value=None,
    )
