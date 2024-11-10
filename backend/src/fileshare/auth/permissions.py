from abc import ABC, abstractmethod
from typing import Type, Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.exceptions import HTTPException

from fileshare.auth.constants import Roles
from fileshare.auth.schemas import UserSchema
from fileshare.auth.service import AuthService

Security = HTTPBearer()


async def get_current_user(service: Annotated[AuthService, Depends()],
                           security: Annotated[HTTPAuthorizationCredentials, Depends(Security)]
                           ) -> UserSchema:
    return await service.get_current_active_user(security.credentials)


class BasePermission(ABC):
    role: Roles = None

    @abstractmethod
    def has_permission(self):
        pass

    async def initialize(self, user: UserSchema) -> UserSchema:
        self.role = user.role
        if not self.has_permission():
            raise HTTPException(status_code=401, detail='Invalid permissions')
        return user


class AdminPermission(BasePermission):
    def has_permission(self):
        return self.role == Roles.ADMIN


class UserPermission(BasePermission):
    def has_permission(self):
        return self.role == Roles.USER


class AllPermissions(BasePermission):
    def has_permission(self):
        return True


class PermissionDependency:
    def __init__(self, permission_class: Type[BasePermission]):
        self.permission_class = permission_class

    async def __call__(self, user: Annotated[UserSchema, Depends(get_current_user)]):
        return await self.permission_class().initialize(user)


AuthenticatedPermissionsDependency = Annotated[UserSchema, Depends(PermissionDependency(AllPermissions))]
AdminPermissionDependency = Annotated[UserSchema, Depends(PermissionDependency(AdminPermission))]
