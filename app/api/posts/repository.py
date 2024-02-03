from app.api.common.repository import DependableBaseRepository
from app.models import Post


class PostRepository(DependableBaseRepository):
    model = Post
    dependency_field = Post.user_id
