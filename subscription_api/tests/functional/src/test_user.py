from http import HTTPStatus

import pytest

SUBSCRIPTION_ID = '429b436a-d042-4e3e-84e5-789204a33042'
DETAILS = {
    'id': '429b436a-d042-4e3e-84e5-789204a33042',
    'user_id': 'a49b436a-d0b3-4e3e-84e5-ac9204a33042',
    'product': {
        'id': 'a49b436a-d0b3-4e3e-84e5-ac9204a330a5',
        'price': 20000,
        'currency_code': 'RUB',
        'period': 30,
        'is_active': True
    },
    'start_date': '2021-10-15',
    'end_date': '2021-11-14',
    'state': 'active'
}


@pytest.mark.asyncio
async def test_user_get_subscriptions(headers, api_url, make_get_request):
    url = f"{api_url}/user/subscription"
    response = await make_get_request(url, headers=headers)

    assert response.status == HTTPStatus.OK, "Couldn't get user subscriptions"
    assert len(response.body) == 5, "Incorrect number of subscriptions"


@pytest.mark.asyncio
async def test_user_get_subscription_details(headers, api_url, make_get_request):
    url = f"{api_url}/user/subscription/{SUBSCRIPTION_ID}"

    response = await make_get_request(url, headers=headers)
    assert response.status == HTTPStatus.OK, "Couldn't get subscription_details"

    # NOTE I'm not sure if this is a safe way. Maybe use a deep distinction
    assert response.body == DETAILS


@pytest.mark.asyncio
async def test_unauth_user_get_subscription_details(api_url, make_get_request):
    url = f"{api_url}/user/subscription/{SUBSCRIPTION_ID}"

    response = await make_get_request(url)
    assert response.status == HTTPStatus.FORBIDDEN, "Unauth user got subscription"


@pytest.mark.asyncio
async def test_user_cancel_subscription(headers, api_url, make_delete_request):
    url = f"{api_url}/user/subscription/{SUBSCRIPTION_ID}"
    response = await make_delete_request(url, headers=headers)
    assert response.status == HTTPStatus.OK, "Couldn't cancel subscription"
    assert response.body['state'] == 'cancelled', "Subscription state didn't change"


@pytest.mark.asyncio
async def test_user_refund_subscription(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/product/active")
    assert response.status == HTTPStatus.OK, "Couldn't get active products."


@pytest.mark.asyncio
async def test_get_access_for_product(headers, api_url, make_get_request):
    product = "a49b436a-d0b3-4e3e-84e5-ac9204a330a5"
    url = f"{api_url}/user/product/{product}"

    response = await make_get_request(url, headers=headers)
    assert response.status == HTTPStatus.OK, "User don't have access for product"


@pytest.mark.asyncio
async def test_not_get_access_for_product(headers, api_url, make_get_request):
    product = "a49b436a-d0b3-4e3e-84e5-ac9204a33666"
    url = f"{api_url}/user/product/{product}"

    response = await make_get_request(url, headers=headers)
    assert response.status == HTTPStatus.NOT_FOUND, "User get access for fake product"


@pytest.mark.asyncio
async def test_get_refund(headers, api_url, make_post_request):
    subscription = '429b436a-d042-4e3e-84e5-789204a33042'
    url = f"{api_url}/user/refund/{subscription}"

    response = await make_post_request(url, headers=headers)
    assert response.status == HTTPStatus.OK, "User couldn't refund subscription"


@pytest.mark.asyncio
async def test_get_refund_wrong(headers, api_url, make_post_request):
    subscription = '429b436a-6666-6666-84e5-789204a33042'
    url = f"{api_url}/user/refund/{subscription}"

    response = await make_post_request(url, headers=headers)
    assert response.status == HTTPStatus.NOT_FOUND, "User could refund fake subscription"
