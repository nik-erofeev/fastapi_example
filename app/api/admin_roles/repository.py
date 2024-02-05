from app.api.common.repository import BaseRepository, BaseSearchMixin
from app.models import User


class AdminRoleRepository(BaseRepository, BaseSearchMixin):
    model = User
