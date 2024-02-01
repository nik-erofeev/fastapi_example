from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app import models
from app.database import Base


class Users(models.IdMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(250), nullable=False)
