from typing import Annotated

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends
from starlette.responses import StreamingResponse

from fileshare.auth.permissions import AdminPermissionDependency, AuthenticatedPermissionsDependency
from fileshare.auth.schemas import UserSchema
from fileshare.files.schemas import FileIn
from fileshare.files.service import FilesService
from fastapi.responses import FileResponse

file_router = APIRouter()

FilesService = Annotated[FilesService, Depends()]


@file_router.get("")
async def get_files(user: Annotated[UserSchema, AuthenticatedPermissionsDependency], service: FilesService):
    return await service.get_files(user)


@file_router.post("/permissions/{file_id}/{user_id}", dependencies=[AdminPermissionDependency])
async def give_permissions(file_id: int, user_id: int, service: FilesService):
    await service.give_permissions(file_id, user_id)
    return {"message": "Permissions given to user {} ".format(user_id)}


@file_router.delete("/permissions/{file_id}/{user_id}", dependencies=[AdminPermissionDependency])
async def remove_permissions(file_id: int, user_id: int, service: FilesService):
    await service.remove_permissions(file_id, user_id)
    return {"message": "Permissions removed from user {} ".format(user_id)}


@file_router.get("/download/{file_id}")
async def download_file(file_id: Annotated[int, "File id"],
                        user: Annotated[UserSchema, AuthenticatedPermissionsDependency],
                        service: FilesService):
    file, path = await service.get_file(file_id, user)
    return FileResponse(path, media_type=file.content_type, filename=file.name)

@file_router.post("/upload", status_code=201)
async def upload_file(file: UploadFile, user: Annotated[UserSchema, AdminPermissionDependency], service: FilesService):
    file_content = await file.read()
    file_in = FileIn(owner_id=user.id, **file.__dict__, content_type=file.content_type, content=file_content)
    response = await service.upload_file(file_in)
    return {"massage": f"File successfully uploaded: {response}"}
