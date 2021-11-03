"""
Auth integration
"""

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.config import settings

oauth_schema = HTTPBearer()


async def auth(authorization: HTTPAuthorizationCredentials = Depends(oauth_schema)):
    try:
        payload = jwt.decode(authorization.credentials,
                             settings.jwt_secret_key,
                             algorithms=[settings.jwt_algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User id not found")
        return user_id
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})


def get_auth():
    if settings.debug:
        return '3fa85f64-5717-4562-b3fc-2c963f66afa6'

    return auth
