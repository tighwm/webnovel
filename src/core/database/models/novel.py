from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.database.models import User


class Novel(Base, IdIntPkMixin):
    title: Mapped[str] = mapped_column(nullable=False, index=True, unique=False)
    description: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="novels")
