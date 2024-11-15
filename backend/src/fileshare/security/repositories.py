from datetime import timezone
from uuid import UUID

from sqlalchemy import insert, select, update
from datetime import datetime

from fileshare.database.core import DBSession
from fileshare.security.models import Token
from fileshare.security.schemas import TokenInDbSchema, TokenSchema


class TokenRepository:
    def __init__(self, session: DBSession):
        self._session = session
        self._model = Token

    async def create(self, token: TokenInDbSchema):
        stmt = insert(self._model).values(**token.model_dump()).returning(self._model.id)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalar_one()

    async def revoke_all_not_expired_by_user(self, user_id):
        stmt = (update(self._model)
                .where
                    (
                    (self._model.user_id == user_id) &
                    (self._model.expires_at >= datetime.now(timezone.utc).replace(tzinfo=None)) &
                    (~self._model.revoked)
                )
                .values(revoked=True)
                .returning(self._model.id))
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.scalars().all()

    async def get_by_id(self, token_id: UUID):
        stmt = select(self._model).where(self._model.id == token_id)
        result = await self._session.execute(stmt)
        token = result.scalar_one_or_none()
        return TokenSchema.model_validate(token) if token else None
