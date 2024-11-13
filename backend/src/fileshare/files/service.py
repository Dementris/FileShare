from importlib.metadata import files
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends

from fileshare.auth.constants import Roles
from fileshare.auth.repositories import UserRepository
from fileshare.auth.schemas import UserSchema
from fileshare.auth.service import UserService
from fileshare.files.constants import Permissions
from fileshare.files.repositories import FilesRepository, FilePermissionsRepository
from fileshare.files.schemas import FileIn, FileResponseSchema, FileSchema
from fileshare.storage.core import FileStorage


class FilesService:
    def __init__(self,
                 repository: Annotated[FilesRepository, Depends()],
                 storage: Annotated[FileStorage, Depends()],
                 user_repository: Annotated[UserRepository, Depends()],
                 permissions_repository: Annotated[FilePermissionsRepository, Depends()]):
        self._file_repository = repository
        self._permissions_repository = permissions_repository
        self._storage = storage
        self._user_repository = user_repository

    async def upload_file(self, file: FileIn):
        file.location = self._storage.save_file(file.content).__str__()
        if not file.location:
            raise HTTPException(400, "Provide a location")
        return await self._file_repository.create(file)

    async def get_files(self, user: UserSchema):
        if user.role is Roles.ADMIN:
            files = await self._file_repository.get_all_files()
            return [FileResponseSchema(**file.model_dump()) for file in files]
        else:
            files = await self._file_repository.get_files_by_user_access(user.id)
            return [FileResponseSchema(**file.model_dump()) for file in files]


    async def give_permissions(self, file_id, user_id):
        user = await self._user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        permission = await self._permissions_repository.get_permissions_by_file_and_user(file_id, user_id)
        if permission:
            raise HTTPException(403, "User already has permission")
        await self._permissions_repository.add_permission_to_user(file_id, user_id)

    async def remove_permissions(self, file_id, user_id):
        user = await self._user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        permission = await self._permissions_repository.get_permissions_by_file_and_user(file_id, user_id)
        if not permission:
            raise HTTPException(status_code=403, detail='Permission not found')
        await self._permissions_repository.delete_permission_from_user(file_id, user_id)

    async def get_file(self, file_id, user: UserSchema):
        if user.role is Roles.ADMIN:
            file = await self._file_repository.get_file_by_id(file_id)
        else:
            file = await self._file_repository.get_file_by_id_and_user(file_id, user.id)

        if not file:
            raise HTTPException(status_code=404, detail='File not found or you do not have permission')
        else:
            return self._storage.get_file(file.location)
