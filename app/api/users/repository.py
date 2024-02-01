from app.api.common.repository import BaseRepository, BaseSearchMixin
from app.models import User


class UserRepository(BaseRepository, BaseSearchMixin):
    model = User
