from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from starlette import status
from fileshare.auth.schemas import UserCreateSchema, UserLoginSchema, UserResponseSchema, UserLogoutSchema
from .permissions import AuthenticatedPermissionsDependency
from .service import AuthService
from ..security.schemas import TokenResponseSchema

auth_router = APIRouter()
user_router = APIRouter()

AuthService = Annotated[AuthService, Depends()]


@auth_router.post("/login",
                  status_code=status.HTTP_200_OK,
                  response_model=UserResponseSchema)
async def login(request: UserLoginSchema, service: AuthService):
    user = await service.login_user(request)
    return user

@auth_router.get("/logout",
                 status_code=status.HTTP_200_OK,
                 response_model=UserLogoutSchema)
async def logout(service: AuthService, user: AuthenticatedPermissionsDependency):
    await service.logout_user(user)
    return UserLogoutSchema()

@auth_router.get("/refresh",
                 status_code=status.HTTP_200_OK,
                 response_model=TokenResponseSchema)
async def refresh_tokens(service: AuthService, user: AuthenticatedPermissionsDependency):
    return await service.refresh_token(user)

@auth_router.post("/create_user",
                  status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateSchema, service: AuthService):
    user = await service.create_user(request)
    return {"message": f"user created with id = {user}"}


@user_router.get("/me")
async def get_current_user(user: AuthenticatedPermissionsDependency):
    return user
