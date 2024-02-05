from logging import getLogger

from fastapi import APIRouter

from app.api.admin_roles.services import AdminRoleService
from app.api.users.schemas import UserResponseTest


logger = getLogger(__name__)

router = APIRouter(prefix="/roles", tags=["Роли Админов"])


@router.patch("/{user_id}", response_model=UserResponseTest)
async def patch_admin_privilege(user: AdminRoleService.grand_admin_privilege_dep):
    return user


@router.delete("/{user_id}", response_model=UserResponseTest)
async def delete_admin_privilege(user: AdminRoleService.revoke_admin_privileges_dep):
    return user
