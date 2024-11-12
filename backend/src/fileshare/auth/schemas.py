from datetime import datetime

from pydantic import EmailStr, field_validator, SecretStr, Field

from fileshare.auth.constants import Roles
from fileshare.auth.utils import hash_password, is_hash
from fileshare.schemas import FileShareBase
from fileshare.security.schemas import TokenResponseSchema


class UserLoginSchema(FileShareBase):
    email: EmailStr
    password: str

class UserLogoutSchema(FileShareBase):
    message: str = "User successfully logged out."


class UserCreateSchema(UserLoginSchema):
    username: str

    @field_validator("password")
    @classmethod
    def password_required(cls, value: str) -> str:
        return hash_password(value) if not is_hash(value) else value


class UserSchema(FileShareBase):
    id: int
    username: str
    email: EmailStr
    password: str
    role: Roles
    created_at: datetime
    updated_at: datetime
    disabled: bool

class UserResponseSchema(FileShareBase):
    id: int
    username: str
    email: EmailStr
    role: Roles
    created_at: datetime
    updated_at: datetime

class UserLoginResponseSchema(UserResponseSchema):
    token: TokenResponseSchema
