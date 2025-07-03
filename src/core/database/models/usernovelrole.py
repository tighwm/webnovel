from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.database.models import User, Novel, Role


class UserNovelRole(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="novel_roles")
    novel: Mapped["Novel"] = relationship(back_populates="user_roles")
    role: Mapped["Role"] = relationship(back_populates="user_assignments")
