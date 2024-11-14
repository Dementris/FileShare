from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, UploadFile
from fastapi.params import Depends
from starlette.responses import StreamingResponse

from fileshare.auth.permissions import AdminPermissionDependency, AuthenticatedPermissionsDependency
from fileshare.auth.schemas import UserSchema
from fileshare.config import settings
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
    file_id = await service.get_file(file_id, user)
    return {'downloadUrl': settings.BASE_URL + f"/files/link/{str(file_id)}"}


@file_router.get("/link/{temp_file}")
async def download_link(temp_file: UUID, service: FilesService):
    tem_file = await service.get_temp_file(temp_file)
    path = tem_file.temp_file_path
    def iter_file():
        with open(path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # 1MB chunks
                yield chunk

    return StreamingResponse(
        iter_file(),
        media_type=tem_file.file.content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{tem_file.file.name}"'
        }
    )

@file_router.post("/upload", status_code=201)
async def upload_file(files: list[UploadFile], user: Annotated[UserSchema, AdminPermissionDependency],
                      service: FilesService):
    for file in files:
        file_content = await file.read()
        file_in = FileIn(owner_id=user.id, **file.__dict__, content_type=file.content_type, content=file_content)
        await service.upload_file(file_in)

    return {"massage": f"Files successfully uploaded"}
