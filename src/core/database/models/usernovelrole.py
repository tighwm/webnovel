from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin


class UserNovelRole(Base, IdIntPkMixin):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    novel_id: Mapped[int] = mapped_column(ForeignKey("novels.id"), nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
