from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import models
from app.database import Base


class Product(models.IdMixin, Base):
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
