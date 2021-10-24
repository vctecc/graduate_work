import pytest

PREFIX = "service/orders"


@pytest.mark.asyncio
async def test_get_active_orders(api_url, make_get_request):
    url = f'{api_url}/{PREFIX}'

    response = await make_get_request(url)
    assert response.status == 200, "Couldn't get orders."
    assert len(response.body) == 2

    # response = await make_get_request(url)
    # assert response.status == 404, "Orders received twice"
