from sqlalchemy.exc import NoResultFound

from app.api.users.exceptions import http_superadmin_conflict_exception, http_user_not_found_exception
from app.api.users.repository import UserRepository
from app.api.users.schemas import UserByUsernameRequest
from app.database import SessionDep
from app.models import PortalRole, User


async def user_by_username(
    user_data: UserByUsernameRequest,
    session: SessionDep,
):
    search_select = UserRepository.search(username=user_data.username)

    result = await session.scalar(search_select)

    try:
        return result

    except NoResultFound:
        raise http_user_not_found_exception


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if current_user is None:
        return False

    if PortalRole.SUPERADMIN in current_user.roles:
        raise http_superadmin_conflict_exception

    if target_user.id != current_user.id:
        # Check if current user has ADMIN or SUPERADMIN role
        if current_user.roles not in {PortalRole.ADMIN, PortalRole.SUPERADMIN}:
            return False

        # Check if current user is trying to deactivate a SUPERADMIN
        if PortalRole.SUPERADMIN in target_user.roles and current_user.roles == PortalRole.ADMIN:
            return False

        # Check if current user is trying to deactivate an ADMIN
        if PortalRole.ADMIN in target_user.roles and current_user.roles == PortalRole.ADMIN:
            return False
    return True
