from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel

from fileshare.auth.routes import auth_router, user_router
from fileshare.files.routes import file_router
from fastapi.middleware.gzip import GZipMiddleware

class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


app = FastAPI(debug=True, root_path="/api/v1")

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5) # noqa

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(file_router, prefix="/files", tags=["files"])

