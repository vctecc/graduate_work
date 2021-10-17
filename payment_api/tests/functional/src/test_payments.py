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
async def test_get_processing_payments(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/payments/processing")
    assert response.status == 200, "Couldn't get processing payments."


@pytest.mark.asyncio
async def test_update_payment_status(api_url, make_patch_request):
    payment_id = "1"
    status = "paid"
    response = await make_patch_request(f"{api_url}/payments/{payment_id}/status?status={status}")
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
