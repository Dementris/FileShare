from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from starlette import status
from fileshare.auth.schemas import UserCreateSchema, UserLoginSchema, UserLoginResponseSchema, UserLogoutSchema, \
    UserResponseSchema, UserSchema
from .permissions import AuthenticatedPermissionsDependency, AdminPermissionDependency, AdminPermission, \
    PermissionDependency
from .service import AuthService, UserService
from ..security.schemas import TokenResponseSchema

auth_router = APIRouter()
user_router = APIRouter()

AuthService = Annotated[AuthService, Depends()]
UserService = Annotated[UserService, Depends()]


@auth_router.post("/login",
                  status_code=status.HTTP_200_OK,
                  response_model=UserLoginResponseSchema)
async def login(request: UserLoginSchema, service: AuthService):
    user = await service.login_user(request)
    return user

@auth_router.get("/logout",
                 status_code=status.HTTP_200_OK,
                 response_model=UserLogoutSchema)
async def logout(service: AuthService, user: Annotated[UserSchema, AuthenticatedPermissionsDependency]):
    await service.logout_user(user)
    return UserLogoutSchema()

@auth_router.get("/refresh",
                 status_code=status.HTTP_200_OK,
                 response_model=TokenResponseSchema)
async def refresh_tokens(service: AuthService, user: Annotated[UserSchema, AuthenticatedPermissionsDependency]):
    return await service.refresh_token(user)

@user_router.post("/create_user",
                  status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateSchema, service: UserService):
    user = await service.create_user(request)
    return {"message": f"user created with id = {user}"}


@user_router.get("/me")
async def get_current_user(user: Annotated[UserSchema, AuthenticatedPermissionsDependency]):
    return UserResponseSchema.model_validate(user)

@user_router.get("", dependencies=[AdminPermissionDependency])
async def get_users(service: UserService):
    response = await service.get_all_users()
    return response

@user_router.get("/{user_id}", dependencies=[AdminPermissionDependency])
async def get_user(user_id: int, service: UserService):
    response = await service.get_user(user_id)
    return response

@user_router.get("/permission/{file_id}", dependencies=[AdminPermissionDependency])
async def get_users_with_permission(file_id: int, service: UserService):
    response = await service.get_user_with_permission(file_id=file_id)
    return response

@user_router.get("/permission/not/{file_id}", dependencies=[AdminPermissionDependency])
async def get_users_without_permission(file_id: int, service: UserService):
    response = await service.get_user_without_permission(file_id=file_id)
    return response