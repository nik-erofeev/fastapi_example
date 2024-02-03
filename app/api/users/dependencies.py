from fastapi import Depends

from app.api.auth.utils import get_current_user
from app.api.users.exceptions import http_role_conflict_exception
from app.api.users.services import UserService
from app.api.users.utils import check_user_permissions
from app.database import SessionDep
from app.models import User


async def check_user_permissions_dependency(
    user_id: int,
    session: SessionDep,
    current_user: User = Depends(get_current_user),
):
    target_user = await UserService.get(user_id, session=session)

    if not check_user_permissions(target_user, current_user):
        raise http_role_conflict_exception

    return target_user
