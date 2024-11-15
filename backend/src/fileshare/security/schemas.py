from datetime import datetime, timezone

from pydantic import EmailStr, Field, AliasChoices
from uuid import UUID
from fileshare.auth.constants import Roles
from fileshare.schemas import FileShareBase


class TokenInDbSchema(FileShareBase):
    id: str = Field(validation_alias=AliasChoices("id","jti"))
    user_id: int = Field(validation_alias=AliasChoices("user_id","sub"))
    expires_at: datetime = Field(validation_alias=AliasChoices("expires_at","exp"))
    revoked: bool = False


class Payload(FileShareBase):
    sub: int
    username: str
    email: EmailStr
    role: Roles
    jti: str
    exp: datetime


class TokenSchema(TokenInDbSchema):
    created_at: datetime

    @property
    def expired(self):
        return self.expires_at < datetime.now(timezone.utc).replace(tzinfo=None)


class TokenResponseSchema(FileShareBase):
    accessToken: str
    refreshToken: str