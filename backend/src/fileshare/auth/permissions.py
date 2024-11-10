from abc import ABC, abstractmethod
from typing import Annotated, Type

from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.exceptions import HTTPException

from fileshare.auth.constants import Roles
from fileshare.auth.schemas import UserSchema
from fileshare.security.service import JwtSecurityService

Security = HTTPBearer()

Service = Annotated[JwtSecurityService, Depends()]


class BasePermission(ABC):
    role: Roles = None

    @abstractmethod
    def has_permission(self):
        pass

    async def initialize(self, service: JwtSecurityService, security: HTTPAuthorizationCredentials):
        user = await self.me(service, security)
        self.role = user.role
        if not self.has_permission():
            raise HTTPException(status_code=401, detail='Invalid permissions')

    @staticmethod
    async def me(service: Service, security: Annotated[HTTPAuthorizationCredentials, Depends(Security)]) -> UserSchema:
        return await service.get_current_active_user(security.credentials)


CurrentUser = Annotated[UserSchema, Depends(BasePermission.me)]


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

    async def __call__(self, service: Service, security: Annotated[HTTPAuthorizationCredentials, Depends(Security)]):
        await self.permission_class().initialize(service, security)
