from app.api.common.repository import BaseRepository, BaseSearchMixin
from app.models import Product


class ProductRepository(BaseRepository, BaseSearchMixin):
    model = Product
