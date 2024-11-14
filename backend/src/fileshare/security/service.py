from typing import Annotated

from fastapi.params import Depends
from starlette.exceptions import HTTPException

from fileshare.auth.schemas import UserSchema
from fileshare.security.repositories import TokenRepository
from fileshare.security.schemas import TokenInDbSchema, TokenResponseSchema, TokenSchema
from fileshare.security.utils import create_token, decode_token


class JwtSecurityService:
    def __init__(self, jwt_repository: Annotated[TokenRepository, Depends()]):
        self._jwt_repository = jwt_repository

    async def create_access_refresh_token(self, user: UserSchema) -> TokenResponseSchema:
        access_token, payload = create_token(user)
        await self._jwt_repository.create(TokenInDbSchema(**payload.model_dump()))
        refresh_token, payload = create_token(user, refresh=True)
        await self._jwt_repository.create(TokenInDbSchema(**payload.model_dump()))
        return TokenResponseSchema(accessToken=access_token, refreshToken=refresh_token)

    async def validate_token(self, token) -> TokenSchema:
        jwt = decode_token(token)
        if not jwt:
            raise HTTPException(status_code=401, detail="Could not validate token")
        tokenindb = TokenInDbSchema(**jwt)
        token = await self._jwt_repository.get_by_id(tokenindb.id)
        if not token:
            raise HTTPException(status_code=401, detail="Could not validate token")
        elif token.expired or token.revoked:
            raise HTTPException(status_code=401,
                                detail="Token has expired or revoked")
        else:
            return token

    async def revoke_user_tokens(self, user: UserSchema):
        tokens = await self._jwt_repository.revoke_all_not_expired_by_user(user.id)
        if not tokens:
            raise HTTPException(status_code=401, detail="Could not logout user")


