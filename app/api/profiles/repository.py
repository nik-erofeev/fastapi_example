from app.api.common.repository import DependableBaseRepository
from app.models import Profile


class ProfileRepository(DependableBaseRepository):
    model = Profile
    dependency_field = Profile.user_id
