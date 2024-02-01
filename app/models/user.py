from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import models
from app.database import Base


class User(models.IdMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
