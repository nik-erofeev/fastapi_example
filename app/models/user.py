from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models
from app.database import Base


class User(models.IdMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[models.PortalRole] = mapped_column(
        Enum(models.PortalRole),
        default=models.PortalRole.USER,
    )

    posts: Mapped[list["models.post.Post"]] = relationship(back_populates="user")

    profile: Mapped["models.profile.Profile"] = relationship(back_populates="user")

    @property
    def is_superadmin(self) -> bool:
        return models.PortalRole.SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return models.PortalRole.ADMIN in self.roles

    def add_admin_privileges_to_model(self):
        if not self.is_admin:
            self.roles = models.PortalRole.ADMIN
        return self.roles

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            self.roles = models.PortalRole.USER
        return self.roles
