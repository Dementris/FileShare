from datetime import timezone
from typing import Annotated

from fastapi.params import Depends
from starlette.exceptions import HTTPException
from win32ctypes.pywin32.pywintypes import datetime

from fileshare.auth.repositories import AuthRepository
from fileshare.auth.schemas import UserSchema
from fileshare.security.repositories import TokenRepository
from fileshare.security.schemas import TokenInDbSchema, TokenResponseSchema
from fileshare.security.utils import create_token, decode_token


class JwtSecurityService:
    def __init__(self,
                 jwt_repository: Annotated[TokenRepository, Depends(TokenRepository)],
                 auth_repository: Annotated[AuthRepository, Depends(AuthRepository)], ):
        self._jwt_repository = jwt_repository
        self._auth_repository = auth_repository

    async def create_access_refresh_token(self, user: UserSchema) -> TokenResponseSchema:
        access_token, payload = create_token(user)
        await self._jwt_repository.create(TokenInDbSchema(**payload.model_dump()))
        refresh_token, payload = create_token(user, refresh=True)
        await self._jwt_repository.create(TokenInDbSchema(**payload.model_dump()))
        return TokenResponseSchema(access_token=access_token, refresh_token=refresh_token)

    async def get_current_active_user(self, token) -> UserSchema:
        jwt = decode_token(token)
        if not jwt:
            raise HTTPException(status_code=401, detail="Could not validate token")
        tokenindb = TokenInDbSchema(**jwt)
        token = await self._jwt_repository.get_by_id(tokenindb.id)
        if not token:
            raise HTTPException(status_code=401, detail="Could not validate token")
        elif token.expired or token.revoked:
            raise HTTPException(status_code=401,
                                detail=f"Token has expired or revoked time from token = {token.expires_at} and from jwt = {tokenindb.expires_at} and"
                                       f"now datetime {datetime.now(timezone.utc)}")
        else:
            return await self._auth_repository.get_user_by_id(token.user_id)
