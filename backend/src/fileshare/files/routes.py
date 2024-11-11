from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from fileshare.auth.permissions import AdminPermission, AllPermissions
from fileshare.files.service import FilesService

file_router = APIRouter()

FilesService = Annotated[FilesService, Depends()]

@file_router.get("")
def get_files(user: AllPermissions, service: FilesService):

    pass

@file_router.get("/{file_id}")
def get_file(user: AllPermissions, service: FilesService):
    pass

@file_router.get("/download/{file_id}")
def download_file(user: AllPermissions, service: FilesService):
    pass

@file_router.post("/upload")
def upload_file(user: AdminPermission, service: FilesService):
    pass

