import pytest


@pytest.mark.asyncio
async def test_new_payment(api_url, headers, make_post_request):
    data = {
        "product": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "currency": "RUB",
    }
    response = await make_post_request(
        f"{api_url}/payments/new/",
        headers=headers,
        data=data
    )
    assert response.status == 201, "Couldn't create payment."


@pytest.mark.asyncio
async def test_accept_payment(api_url, headers, make_patch_request):
    response = await make_patch_request(
        f"{api_url}/payments/pi_3Jm4MeEZwW9AoJC21RnYBpkI/accept",
        headers=headers,
    )
    assert response.status == 200, "Couldn't accept payment."


@pytest.mark.asyncio
async def test_get_processing_payments(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/payments/processing")
    assert response.status == 200, "Couldn't get processing payments."


@pytest.mark.asyncio
async def test_update_payment_status(api_url, make_patch_request):
    data = {
        "id": 12,
        "user_id": "",
        "invoice_id": "pi_3Jm2zYEZwW9AoJC21WBhaYec",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "status": "paid"
    }
    response = await make_patch_request(f"{api_url}/payments/update_status", data=data)
    assert response.status == 200, "Couldn't update payment."


@pytest.mark.asyncio
async def test_add_payment(api_url, headers, make_post_request):
    data = {
        "user_id": "",
        "amount": 100000,
        "product": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5",
        "currency": "RUB",
    }
    response = await make_post_request(
        f"{api_url}/payments/",
        headers=headers,
        data=data
    )
    assert response.status == 201, "Couldn't add payment."


@pytest.mark.asyncio
async def test_cancel(api_url, make_patch_request):

    data = {
        "user_id": "",
        "amount": 10000,
        "currency": "RUB",
    }
    response = await make_patch_request(
        f"{api_url}/payments/cancel",
        data=data
    )
    assert response.status == 201, "Couldn't add payment."
