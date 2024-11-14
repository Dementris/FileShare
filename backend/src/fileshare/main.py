from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel

from fileshare.auth.routes import auth_router, user_router
from fileshare.files.routes import file_router
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


app = FastAPI(debug=True, root_path="/api/v1")

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5) # noqa

app.add_middleware(
    CORSMiddleware, # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["user"])
app.include_router(file_router, prefix="/files", tags=["files"])

