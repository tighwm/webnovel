from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import (
    Permission,
    role_permission_association,
    Role,
    UserNovelRole,
)


async def get_permissions_for_user_to_novel(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
):
    stmt = (
        select(Permission.name)
        .select_from(Permission)
        .join(
            role_permission_association,
            Permission.id == role_permission_association.c.permission_id,
        )
        .join(
            Role,
            role_permission_association.c.role_id == Role.id,
        )
        .join(
            UserNovelRole,
            Role.id == UserNovelRole.id,
        )
        .where(
            and_(
                UserNovelRole.user_id == user_id,
                UserNovelRole.novel_id == novel_id,
            ),
        )
        .distinct()
    )

    result = await session.execute(stmt)

    return result.scalars().all()
