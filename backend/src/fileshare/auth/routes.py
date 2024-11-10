from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from starlette import status
from fileshare.auth.schemas import UserCreateSchema, UserLoginSchema, UserResponseSchema
from .permissions import PermissionDependency, AdminPermission, AllPermissions, CurrentUser
from .service import AuthService

Service = Annotated[AuthService, Depends(AuthService)]

auth_router = APIRouter(tags=["auth"])
user_router = APIRouter(tags=["Users"])


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=UserResponseSchema)
async def login(request: UserLoginSchema, service: Service):
    user = await service.login_user(request)
    return user


@auth_router.post("/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(request: UserCreateSchema, service: Service):
    user = await service.create_user(request)
    return {"message": f"user created with id = {user}"}


@user_router.get("",
                 dependencies=[Depends(PermissionDependency(AdminPermission))], )
async def get_all_users():
    return {"message": 'Hello'}


@user_router.get("/me",
                 dependencies=[Depends(PermissionDependency(AllPermissions))], )
async def get_current_user(user: CurrentUser):
    return user
