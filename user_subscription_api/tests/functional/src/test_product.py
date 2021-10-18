import pytest


@pytest.mark.asyncio
async def test_product_by_id(api_url, make_get_request):
    product_id = "a49b436a-d0b3-4e3e-84e5-ac9204a330a5"
    response = await make_get_request(f"{api_url}/product/{product_id}")
    assert response.status == 200, "Couldn't create review."


@pytest.mark.asyncio
async def test_get_all_products(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/product/")
    assert response.status == 200, "Couldn't get products."
    print(response.body)


@pytest.mark.asyncio
async def test_get_active_products(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/product/active")
    assert response.status == 200, "Couldn't get active products."
