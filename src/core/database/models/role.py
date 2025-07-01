from sqlalchemy.orm import Mapped, mapped_column

from core.database.models import Base
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin


class Role(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
