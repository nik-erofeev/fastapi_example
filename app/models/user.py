from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.database import Base


class User(models.IdMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    posts: Mapped[list["models.post.Post"]] = relationship(back_populates="user")

    profile: Mapped["models.profile.Profile"] = relationship(back_populates="user")
