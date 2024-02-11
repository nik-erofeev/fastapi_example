from logging import getLogger

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from app.api.admin_roles.exceptions import (
    http_admin_or_superadmin_conflict_exception,
    http_current_user_conflict_exception,
    http_no_admin_or_superadmin_conflict_exception,
)
from app.api.admin_roles.repository import AdminRoleRepository
from app.api.auth.utils import get_current_user
from app.api.common.services import BaseService
from app.api.users.exceptions import (
    http_data_conflict_exception,
    http_role_conflict_exception,
    http_superadmin_conflict_exception,
    http_user_not_found_exception,
)
from app.api.users.schemas import UserResponseTest
from app.database import SessionDep
from app.models import User


logger = getLogger(__name__)


class AdminRoleService(BaseService):
    repository = AdminRoleRepository

    @classmethod
    async def grand_admin_privilege(
        cls,
        user_id: int,
        session: SessionDep,
        current_user: User = Depends(get_current_user),
    ):
        if not current_user.is_superadmin:
            raise http_role_conflict_exception

        if current_user.id == user_id:
            raise http_current_user_conflict_exception

        user_for_promotion = await super().get(user_id, session)
        if user_for_promotion.is_admin or user_for_promotion.is_superadmin:
            raise http_admin_or_superadmin_conflict_exception

        if user_for_promotion is None:
            raise http_user_not_found_exception

        updated_user_params = {
            "roles": user_for_promotion.add_admin_privileges_to_model(),
        }
        updated_user_params_model = UserResponseTest(**updated_user_params)

        try:
            update_user = await super().edit(
                user_for_promotion.id,
                updated_user_params_model,
                session,
            )

        except IntegrityError as err:
            logger.error(err)
            raise http_data_conflict_exception

        return UserResponseTest(roles=update_user.roles)

    @classmethod
    @property
    def grand_admin_privilege_dep(cls):
        return cls._dep_get(cls.grand_admin_privilege)

    @classmethod
    async def revoke_admin_privileges(
        cls,
        user_id: int,
        session: SessionDep,
        current_user: User = Depends(get_current_user),
    ):
        if not current_user.is_superadmin:
            raise http_role_conflict_exception

        if current_user.id == user_id:
            raise http_superadmin_conflict_exception

        user_for_revoke_admin_privileges = await super().get(user_id, session)
        if not user_for_revoke_admin_privileges.is_admin:
            raise http_no_admin_or_superadmin_conflict_exception

        if user_for_revoke_admin_privileges is None:
            raise http_user_not_found_exception

        updated_user_params = {
            "roles": user_for_revoke_admin_privileges.remove_admin_privileges_from_model(),
        }

        updated_user_params_model = UserResponseTest(**updated_user_params)

        try:
            update_user = await super().edit(
                user_for_revoke_admin_privileges.id,
                updated_user_params_model,
                session,
            )

        except IntegrityError as err:
            logger.error(err)
            raise http_data_conflict_exception

        return UserResponseTest(roles=update_user.roles)

    @classmethod
    @property
    def revoke_admin_privileges_dep(cls):
        return cls._dep_get(cls.revoke_admin_privileges)
