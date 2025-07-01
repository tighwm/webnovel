import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.database.models import User


class UserSession(Base, IdIntPkMixin):
    jti: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="user_sessions")
