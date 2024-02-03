from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.database import Base


class Post(models.IdMixin, Base):
    title: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["models.user.User"] = relationship(back_populates="posts")
