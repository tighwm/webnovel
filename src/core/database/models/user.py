from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.database.models import UserSession, Novel, UserNovelRole


class User(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    user_sessions: Mapped[list["UserSession"]] = relationship(back_populates="user")
    novels: Mapped[list["Novel"]] = relationship(back_populates="author")
    novel_roles: Mapped[list["UserNovelRole"]] = relationship(back_populates="user")
