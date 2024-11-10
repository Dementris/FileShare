from typing import Annotated

from fastapi.params import Depends
from starlette.exceptions import HTTPException

from fileshare.auth.repositories import AuthRepository
from fileshare.auth.schemas import UserResponseSchema, UserLoginSchema, UserCreateSchema, UserSchema
from fileshare.auth.utils import verify_password
from fileshare.security.service import JwtSecurityService


class AuthService:

    def __init__(self,
                 repository: Annotated[AuthRepository, Depends()],
                 jwt_service: Annotated[JwtSecurityService, Depends()], ):
        self._repository = repository
        self._jwt_service = jwt_service

    async def create_user(self, user: UserCreateSchema):
        entity = await self._repository.get_user_by_email(user.email)
        if entity:
            raise HTTPException(status_code=409, detail='User already exists')
        entity = await self._repository.get_user_by_username(user.username)
        if entity:
            raise HTTPException(status_code=409, detail='User already exists')
        return await self._repository.create(user)

    async def login_user(self, user: UserLoginSchema):
        entity = await self._repository.get_user_by_email(user.email)
        if not entity:
            raise HTTPException(status_code=401, detail='User does not exist')
        pass_valid = verify_password(user.password, entity.password)
        if pass_valid:
            token = await self._jwt_service.create_access_refresh_token(entity)
        else:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        return UserResponseSchema(**entity.model_dump(), token=token)

    async def logout_user(self, user: UserSchema):
        await self._jwt_service.revoke_user_tokens(user)

    async def get_current_active_user(self, credentials):
        validated_credentials = await self._jwt_service.validate_token(credentials)
        return await self._repository.get_user_by_id(validated_credentials.user_id)

    async def refresh_token(self, user):
        await self._jwt_service.revoke_user_tokens(user)
        tokens = await self._jwt_service.create_access_refresh_token(user)
        return tokens
