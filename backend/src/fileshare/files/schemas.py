from datetime import datetime
from typing import BinaryIO

from pydantic import Field, AliasChoices, computed_field

from fileshare.auth.constants import Roles
from fileshare.auth.schemas import UserSchema, UserResponseSchema
from fileshare.files.constants import Permissions
from fileshare.schemas import FileShareBase


class FileSchema(FileShareBase):
    id: int
    name: str = Field(validation_alias=AliasChoices("name", "filename"))
    content_type: str
    location: str
    size: int
    created_at: datetime
    updated_at: datetime
    accessed_at: datetime | None
    deleted: bool
    owner: UserSchema

    permission: Permissions

    @computed_field(return_type=str)
    @property
    def type(self):
        return self.name.split(".")[-1]

class FileOwnerResponseSchema(FileShareBase):
    id: int
    username: str
    email: str
    role: Roles

class FileResponseSchema(FileShareBase):
    id: int
    name: str
    type: str
    size: int
    created_at: datetime
    updated_at: datetime
    owner: FileOwnerResponseSchema
    permission: Permissions


class FileIn(FileShareBase):
    name: str = Field(validation_alias="filename")
    content_type: str
    location: str = None
    size: int
    owner_id: int

    content: bytes = Field(exclude=True)

    @computed_field(return_type=str)
    @property
    def type(self):
        return self.name.split(".")[-1]
