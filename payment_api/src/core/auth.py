"""
Auth integration
"""

import jwt
from src.core.config import settings

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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