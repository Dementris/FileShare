from typing import List

from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from fileshare.auth.models import User
from fileshare.auth.schemas import UserSchema, UserCreateSchema
from fileshare.database.core import DBSession


class UserRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = User

    async def create(self, data: UserCreateSchema) -> int:
        stmt = insert(self._model).values(**data.model_dump())
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.inserted_primary_key[0]

    async def get_user_by_email(self, email: str) -> UserSchema | None:
        stmt = select(self._model).where(self._model.email == email)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserSchema.model_validate(user) if user else None

    async def get_user_by_id(self, user_id: int) -> UserSchema | None:
        stmt = select(self._model).where(self._model.id == user_id)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserSchema.model_validate(user) if user else None

    async def get_user_by_username(self, username: str) -> UserSchema:
        stmt = select(self._model).where(self._model.username == username)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return UserSchema.model_validate(user) if user else None

    async def get_users(self) -> List[UserSchema] | None:
        stmt = select(self._model).order_by(self._model.id)
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return [UserSchema.model_validate(user) for user in users] if users else None

    async def get_users_with_permission(self, file_id):
        stmt = (select(self._model).where(self._model.shared_files.any(id=file_id))
                .options(selectinload(self._model.shared_files)))
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return [UserSchema.model_validate(user) for user in users] if users else None

    async def get_users_without_permission(self, file_id):
        stmt = (select(self._model).where(~self._model.shared_files.any(id=file_id))
                .options(selectinload(self._model.shared_files)))
        result = await self._session.execute(stmt)
        users = result.scalars().all()
        return [UserSchema.model_validate(user) for user in users] if users else None
