from datetime import datetime, timezone
from typing import List

from pydantic_core.core_schema import model_schema
from sqlalchemy import insert, select, delete, literal, literal_column, CHAR, case
from sqlalchemy.orm import selectinload, lazyload, joinedload, subqueryload
from sqlalchemy.testing.plugin.plugin_base import options
from tomlkit import value

from fileshare.auth.constants import Roles
from fileshare.auth.models import User
from fileshare.database.core import DBSession
from fileshare.files.constants import Permissions
from fileshare.files.models import File, files_permissions
from fileshare.files.schemas import FileIn, FileSchema
from sqlalchemy.orm import Load


class FilesRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = File

    async def create(self, file: FileIn) -> int:
        stmt = insert(self._model).values(**file.model_dump()).returning(self._model.id)
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
        .where((self._model.id == file_id) & (~self._model.deleted) & (self._model.user_with_access.any(id=user_id)))
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
        stmt = insert(self._model).values(file_id=file_id, user_id=user_id).returning(self._model.c.file_id)
        await self._session.execute(stmt)
        await self._session.commit()

    async def delete_permission_from_user(self, file_id, user_id):
        stmt = delete(self._model).where(
            (file_id == self._model.c.file_id) & (self._model.c.user_id == user_id))  # noqa
        await self._session.execute(stmt)
        await self._session.commit()
