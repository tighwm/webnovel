from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base, role_permission_association
from core.database.models.mixins.id_int_pk_mixin import IdIntPkMixin

if TYPE_CHECKING:
    from core.database.models import Permission, UserNovelRole


class Role(Base, IdIntPkMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permission_association,
    )
    user_assignments: Mapped["UserNovelRole"] = relationship(back_populates="role")
