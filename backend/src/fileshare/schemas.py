from enum import Enum

from pydantic import BaseModel, ConfigDict



class FileShareBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        json_encoders={
            Enum: lambda v: v.name.lower()
        }
    )

class Pagination(FileShareBase):
    itemsPerPage: int
    page: int
    total: int
