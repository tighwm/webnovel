from sqlalchemy import Table, Column, ForeignKey

from core.database.models import Base

role_permission_association = Table(
    "role_permission_associations",
    Base.metadata,
    Column(
        "role_id",
        ForeignKey("roles.id"),
    ),
    Column(
        "permission_id",
        ForeignKey("permissions.id"),
    ),
)
