import asyncio
from calendar import timegm
from dataclasses import dataclass
from datetime import datetime, timedelta

import aiohttp
import pytest
from jose import jwt
from multidict import CIMultiDictProxy

from .settings import (API_SERVICE_URL, API_VERSION,
                       ALGORITHM, SECRET_KEY, USER_ID)


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
def api_url():
    return f"{API_SERVICE_URL}/api/{API_VERSION}"


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
