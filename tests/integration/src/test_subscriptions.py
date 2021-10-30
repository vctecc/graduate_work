from time import sleep
from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_subscription(
        subscriptions_url,
        payments_url,
        make_get_request,
        make_post_request,
        make_patch_request,
        headers,
):
    data = {
        "user_id": "a49b436a-d0b3-4e3e-84e5-ac9204a33042",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
    }
    url = f"{subscriptions_url}/service/subscription"
    response = await make_post_request(url, data=data)
    assert response.status == HTTPStatus.OK, "Couldn't add subscription."

    # wait for scheduler work
    sleep(3)

    response = await make_get_request(f"{subscriptions_url}/service/orders")
    assert response.status == HTTPStatus.OK, "Couldn't get processing orders."
    assert len(response.body) == 0, "Worker didn't update status."
