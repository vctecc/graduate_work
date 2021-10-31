from http import HTTPStatus

import pytest

PREFIX = "service/orders"


@pytest.mark.asyncio
async def test_get_active_orders(api_url, make_get_request):
    url = f'{api_url}/{PREFIX}'

    response = await make_get_request(url)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 2, "Couldn't get orders."

    response = await make_get_request(url)
    assert response.status == HTTPStatus.OK
    assert len(response.body) == 0, "Get wrong orders numbers."
