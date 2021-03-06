import asyncio
from calendar import timegm
from dataclasses import dataclass
from datetime import datetime, timedelta

import aiohttp
import pytest
import jwt
from multidict import CIMultiDictProxy

from settings import (
    ALGORITHM, SECRET_KEY, USER_ID, SUBSCRIPTION_API_URL,
    SUBSCRIPTION_API_VERSION, PAYMENTS_API_URL, PAYMENTS_API_VERSION
)


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope="session")
def subscriptions_url():
    return f"{SUBSCRIPTION_API_URL}/api/{SUBSCRIPTION_API_VERSION}"


@pytest.fixture(scope="session")
def payments_url():
    return f"{PAYMENTS_API_URL}/{PAYMENTS_API_VERSION}"


@pytest.fixture
async def auth() -> str:
    now = timegm(datetime.utcnow().utctimetuple())
    exp = timegm((datetime.utcnow() + timedelta(minutes=10)).utctimetuple())
    data = {
        'iat': now,
        'jti': 'cf60f579-1cf8-4ca3-8d46-f19e629832d4',
        'type': 'access',
        'sub': USER_ID,
        'nbf': now,
        'exp': exp,
        'role': 'admin'
    }
    return jwt.encode(data, SECRET_KEY, ALGORITHM)


@pytest.fixture
async def headers(auth) -> dict:
    return {"Authorization": f"Bearer {auth}"}


@pytest.fixture
def make_get_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.get(url, json=data, params=params,
                               headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.post(url, json=data, params=params,
                                headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_delete_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.delete(url, json=data, params=params,
                                  headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture
def make_patch_request(session):
    async def inner(url: str, params: dict = None, data: dict = None,
                    headers: dict = None) -> HTTPResponse:
        url = f"http://{url}"
        async with session.patch(url, json=data, params=params,
                                 headers=headers) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner
