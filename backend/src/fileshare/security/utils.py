import logging
import uuid
from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends

from fileshare.auth.repositories import AuthRepository
from fileshare.auth.schemas import UserSchema

from .config import settings


class JwtAuthentication:
    def __init__(self, repository: Annotated[AuthRepository, Depends(AuthRepository)]):
        self.repository = repository

    async def decode_token(self, token: str):
        try:
            token_data = jwt.decode(
                jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return token_data
        except jwt.PyJWTError as e:
            logging.exception(e)
            return None

    async def create_token(self, user: UserSchema, refresh: bool = False):
        payload = {
            "sub": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "jti" : str(uuid.uuid4()),
            "exp": datetime.now(timezone.utc) + (
                timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) if not refresh else timedelta(
                    days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
            ),
        }
        token = jwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return token

