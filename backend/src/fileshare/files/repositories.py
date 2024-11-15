from datetime import datetime, timezone
from typing import List
from uuid import UUID

from pydantic_core.core_schema import model_schema
from sqlalchemy import insert, select, delete, literal, literal_column, CHAR, case
from sqlalchemy.orm import selectinload, lazyload, joinedload, subqueryload
from sqlalchemy.orm.sync import update

from fileshare.auth.schemas import UserWithFileAccessSchema
from fileshare.database.core import DBSession
from fileshare.files.constants import Permissions
from fileshare.files.models import File, files_permissions, TempFile
from fileshare.files.schemas import FileIn, FileSchema, TempFileInSchema, TempFileSchema


class FilesRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = File

    async def create(self, file: FileIn) -> int:
        stmt = insert(self._model).values(**file.model_dump())
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_all_files(self) -> List[FileSchema] | None:
        stmt = (select(self._model)
                .where(~self._model.deleted)
                .options(selectinload(self._model.owner),
                         selectinload(self._model.user_with_access)))
        result = await self._session.execute(stmt)
        files = result.scalars().all()
        return [FileSchema(**file.__dict__, permission=Permissions.DOWNLOAD) for file in files] if files else None

    async def get_files_by_user_access(self, user_id) -> List[FileSchema] | None:
        stmt = ((select(self._model)
                 .where((~self._model.deleted))
                 .options(selectinload(self._model.owner)))
                .options(selectinload(self._model.user_with_access.and_(self._model.user_with_access.any(id=user_id)))))
        result = await self._session.execute(stmt)
        files = result.scalars().all()
        return [
            FileSchema(**file.__dict__, permission=Permissions.DOWNLOAD if file.user_with_access else Permissions.VIEW)
            for file in files] if files else None

    async def get_file_by_id(self, file_id):
        stmt = select(self._model).where((self._model.id == file_id) & (~self._model.deleted)).options(
            selectinload(self._model.owner))
        result = await self._session.execute(stmt)
        file = result.scalar_one_or_none()
        return FileSchema(**file.__dict__, permission=Permissions.DOWNLOAD) if file else None

    async def get_file_by_id_and_user(self, file_id, user_id):
        stmt = (select(self._model)
                .where(
            (self._model.id == file_id) & (~self._model.deleted) & (self._model.user_with_access.any(id=user_id)))
                .options(selectinload(self._model.owner))
                .options(selectinload(self._model.user_with_access.and_(self._model.user_with_access.any(id=user_id)))))
        result = await self._session.execute(stmt)
        file = result.scalar_one_or_none()
        return FileSchema(**file.__dict__, permission=Permissions.DOWNLOAD) if file else None

    async def update_accessed(self, file_id):
        stmt = select(self._model).where((self._model.id == file_id) & (~self._model.deleted))
        result = await self._session.execute(stmt)
        result.scalar_one_or_none().accessed_at = datetime.now(timezone.utc)
        await self._session.commit()

    async def get_users_by_file(self, file_id):
        stmt = (
            select(self._model).where((self._model.id == file_id) & (~self._model.deleted))).options(
            selectinload(self._model.user_with_access))
        result = await self._session.execute(stmt)
        users = result.scalar_one()
        return [UserWithFileAccessSchema.model_validate(user) for user in users.user_with_access] if users else None

    async def set_deleted(self, file_id):
        stmt = select(self._model).where((self._model.id == file_id) & (~self._model.deleted))
        result = await self._session.execute(stmt)
        result.scalar_one().deleted = True
        await self._session.commit()




class FilePermissionsRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = files_permissions

    async def get_permissions_by_file_and_user(self, file_id, user_id):
        stmt = select(self._model).filter(
            (self._model.c.file_id == file_id) & (self._model.c.user_id == user_id))  # noqa
        result = await self._session.execute(stmt)
        permissions = result.scalar_one_or_none()
        return permissions

    async def add_permission_to_user(self, file_id, user_id):
        stmt = insert(self._model).values(file_id=file_id, user_id=user_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_permission_from_user(self, file_id, user_id):
        stmt = delete(self._model).where(
            (file_id == self._model.c.file_id) & (self._model.c.user_id == user_id))  # noqa
        await self._session.execute(stmt)
        await self._session.commit()


class TempFileRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = TempFile

    async def create_temp_file(self, temp_file: TempFileInSchema):
        stmt = insert(self._model).values(**temp_file.model_dump())
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def get_temp_file_by_id(self, id: UUID) -> TempFileSchema:
        stmt = select(self._model).where(self._model.id == id).options(selectinload(self._model.file))
        result = await self._session.execute(stmt)
        temp_file = result.scalar_one_or_none()
        return TempFileSchema.model_validate(temp_file) if temp_file else None
