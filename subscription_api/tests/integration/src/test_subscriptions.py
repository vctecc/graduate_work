from time import sleep

import pytest


@pytest.mark.asyncio
async def test_subscription_update(
        subscriptions_url,
        payments_url,
        make_get_request,
        make_post_request,
        make_patch_request,
        headers,
):

    data = {
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "amount": 100000,
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "currency": "RUB",
    }
    response = await make_post_request(
        f"{payments_url}/payments/",
        data=data
    )
    assert response.status == 201, "Couldn't add payment."

    # wait for scheduler work
    sleep(40)

    response = await make_get_request(f"{payments_url}/payments/processing")
    assert response.status == 200, "Couldn't get processing payments."
    assert len(response.body) == 0, "Worker didn't update status."

    # Get user subscription
    url = f"{subscriptions_url}/user/subscription"
    response = await make_get_request(url, headers=headers)

    assert response.status == 200, "Couldn't get user subscriptions"
    assert len(response.body) == 3, "Incorrect number of subscriptions"
