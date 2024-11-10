from typing import Annotated

from fastapi.params import Depends
from starlette.exceptions import HTTPException

from fileshare.auth.repositories import AuthRepository
from fileshare.auth.schemas import UserResponseSchema, UserLoginSchema, UserCreateSchema
from fileshare.auth.utils import verify_password
from fileshare.security.service import JwtSecurityService


class AuthService:

    def __init__(self,
                 repository: Annotated[AuthRepository, Depends(AuthRepository)],
                 jwt_service: Annotated[JwtSecurityService, Depends(JwtSecurityService)], ):
        self._user_repository = repository
        self._jwt_service = jwt_service

    async def create_user(self, user: UserCreateSchema):
        entity = await self._user_repository.get_user_by_email(user.email)
        if entity:
            raise HTTPException(status_code=409, detail='User already exists')
        entity = await self._user_repository.get_user_by_username(user.username)
        if entity:
            raise HTTPException(status_code=409, detail='User already exists')

        return await self._user_repository.create(user)

    async def login_user(self, user: UserLoginSchema):
        entity = await self._user_repository.get_user_by_email(user.email)
        if not entity:
            raise HTTPException(status_code=401, detail='User does not exist')
        pass_valid = verify_password(user.password, entity.password)
        if pass_valid:
            token = await self._jwt_service.create_access_refresh_token(entity)
        else:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        return UserResponseSchema(**entity.model_dump(), token=token)
