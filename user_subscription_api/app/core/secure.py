import logging

import backoff
from aiohttp import ClientConnectorError, ClientSession, ServerConnectionError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from .config import settings

logger = logging.getLogger(__name__)
oauth_schema = HTTPBearer()


class GetPubKeyError(Exception):
    pass


class User:
    def __init__(self, payload: dict):
        self._id = payload["sub"]
        self._role = payload["role"]

    @property
    def id(self):
        return self._id

    def is_admin(self) -> bool:
        return "admin" == self._role


@backoff.on_exception(
    backoff.expo,
    (ClientConnectorError, ServerConnectionError, GetPubKeyError),
    base=settings.backoff.base,
    factor=settings.backoff.factor,
    max_value=settings.backoff.max_value,
)
async def get_public_key(url: str) -> str:
    async with ClientSession() as session, session.get(url) as resp:
        if resp.status != 200:
            logger.error("Error while getting public key from auth service")
            raise GetPubKeyError()

        body = resp.json()
        return body["public_key"]


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(oauth_schema)) -> User:
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise exception

    try:
        # FIXME use get_public_key instead settings.auth.secret_key
        payload = jwt.decode(token.credentials,
                             settings.auth.secret_key,
                             algorithms=[settings.auth.algorithm])
    except JWTError:
        raise exception

    try:
        return User(payload)
    except KeyError:
        raise exception
