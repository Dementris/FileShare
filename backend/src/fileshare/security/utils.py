import logging
import uuid
from datetime import datetime, timezone, timedelta

import jwt
from fileshare.auth.schemas import UserSchema

from .config import settings
from .schemas import Payload


def decode_token(token: str):
    try:
        token_data = jwt.decode(
            jwt=token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e.args)
        return None


def create_token(user: UserSchema, refresh: bool = False):
    payload = Payload(
        sub=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        jti=str(uuid.uuid4()),
        exp=datetime.now(timezone.utc) + (
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) if not refresh else timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        ),
    )
    token = jwt.encode(payload.model_dump(), key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, payload
