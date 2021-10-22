import pytest


@pytest.mark.asyncio
async def test_new_payment(
        subscriptions_url,
        payments_url,
        make_get_request,
        make_post_request,
        make_patch_request
):
    response = await make_post_request(f'{payments_url}/payments/new')
    response = await make_patch_request(f'{payments_url}/payments/{payment_id}/accept')
    response = await make_get_request(f'{subscriptions_url}/subscription')


@pytest.mark.asyncio
async def test_add_payment(
        subscriptions_url,
        payments_url,
        make_get_request,
        make_post_request,
        make_patch_request
):
    response = await make_post_request(f'{payments_url}/payments')
    response = await make_get_request(f'{payments_url}/payments/processing')
    # wait for scheduler work
    response = await make_get_request(f'{subscriptions_url}/subscription')


@pytest.mark.asyncio
async def test_subscription(
        subscriptions_url,
        payments_url,
        make_get_request,
        make_post_request,
        make_patch_request
):
    response = await make_post_request(f'{payments_url}/payments')
    response = await make_get_request(f'{payments_url}/payments/processing')
    # wait for scheduler work
    response = await make_get_request(f'{subscriptions_url}/subscription')