from datetime import datetime, timedelta
import pytest

PREFIX = "service/subscription"
DETAILS = {
    'id': '429b436a-d0b3-4e3e-84e5-ac9204a33042',
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
async def test_get_subscription_details(api_url, make_get_request):
    _id = '429b436a-d0b3-4e3e-84e5-ac9204a33042'
    url = f"{api_url}/{PREFIX}/{_id}"
    response = await make_get_request(url)
    assert response.status == 200, "Couldn't get subscription_details"

    # NOTE I'm not sure if this is a safe way. Maybe use a deep distinction
    assert response.body == DETAILS


@pytest.mark.asyncio
async def test_inactivate_subscription(api_url, make_delete_request):
    _id = "429b436a-d0b3-4e3e-84e5-ac9204a33042"
    url = f"{api_url}/{PREFIX}/{_id}"

    response = await make_delete_request(url)
    assert response.status == 200, "Couldn't inactivate subscription"
    assert response.body['state'] == 'inactive'


@pytest.mark.asyncio
async def test_activate_subscription(api_url, make_post_request):
    _id = '429b436a-d0b3-4e3e-84e5-ac9204a33042'
    url = f"{api_url}/{PREFIX}/{_id}"

    response = await make_post_request(url)
    assert response.status == 200, "Couldn't get activate subscription"
    assert response.body['state'] == 'active'

    end_data = datetime.now() + timedelta(days=30)
    assert response.body['end_date'] == f"{end_data:%Y-%m-%d}"


@pytest.mark.asyncio
async def test_active_subscription_with_custom_period(api_url, make_post_request):
    _id = "429b436a-d0b3-4e3e-84e5-ac9204a33042"
    url = f"{api_url}/{PREFIX}/{_id}"
    period = 10

    response = await make_post_request(url, params={"period": period})
    assert response.status == 200, "Couldn't change subscription period"
    assert response.body['state'] == 'active'

    end_data = datetime.now() + timedelta(days=period)
    assert response.body['end_date'] == f"{end_data:%Y-%m-%d}"


@pytest.mark.asyncio
async def test_create_subscription(api_url, make_post_request):
    url = f"{api_url}/{PREFIX}"
    new = {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "product_id": "a49b436a-d0b3-4e3e-84e5-ac9204a330a5"
    }

    response = await make_post_request(url, data=new)
    assert response.status == 200, "Couldn't create new subscription"
    assert response.body['state'] == 'active'

    end_data = datetime.now() + timedelta(days=30)
    assert response.body['end_date'] == f"{end_data:%Y-%m-%d}"
