import asyncio
from dataclasses import dataclass

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from .settings import API_SERVICE_URL, API


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
    return f"{API_SERVICE_URL}/{API}"


@pytest.fixture(scope="session")
async def auth() -> str:
    return ''


@pytest.fixture(scope="session")
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