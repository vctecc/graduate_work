import pytest


@pytest.mark.asyncio
async def test_new_payment(
        subscriptions_url,
        payments_url,
        headers,
        make_get_request,
        make_post_request,
        make_patch_request
):
    # Create payment
    data = {
        "product": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "currency": "RUB",
    }
    response = await make_post_request(
        f"{payments_url}/payments/new/",
        headers=headers,
        data=data
    )
    assert response.status == 201, "Couldn't create payment."

    # Update status for created payment
    data = {
        "invoice_id": "pi_3JnrIvEZwW9AoJC20hPPg3ua",
        "status": "paid"
    }
    response = await make_patch_request(f"{payments_url}/payments/update_status", data=data)
    assert response.status == 200, "Couldn't update payment."

    # Get user subscription
    url = f"{subscriptions_url}/user/subscription"
    response = await make_get_request(url, headers=headers)

    assert response.status == 200, "Couldn't get user subscriptions"
    assert len(response.body) == 3, "Incorrect number of subscriptions"


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