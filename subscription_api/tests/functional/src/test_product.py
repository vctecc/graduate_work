from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_product_by_id(api_url, make_get_request):
    product_id = "a49b436a-d0b3-4e3e-84e5-ac9204a330a5"
    response = await make_get_request(f"{api_url}/product/{product_id}")
    assert response.status == HTTPStatus.OK, "Couldn't get product."


@pytest.mark.asyncio
async def test_get_all_products(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/product/")
    assert response.status == HTTPStatus.OK, "Couldn't get products."
    assert len(response.body) == 2, "Incorrect number of products."


@pytest.mark.asyncio
async def test_get_active_products(api_url, make_get_request):
    response = await make_get_request(f"{api_url}/product/active")
    assert response.status == HTTPStatus.OK, "Couldn't get active products."
    assert len(response.body) == 1, "Incorrect number of active products."
