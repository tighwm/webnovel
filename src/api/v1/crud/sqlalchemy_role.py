from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.usernovelrole import UserNovelRoleCreate
from core.database.models import (
    Role,
    UserNovelRole,
    Permission,
    role_permission_association,
)


async def create_unr(
    session: AsyncSession,
    unr_in: UserNovelRoleCreate,
):
    urn_orm = UserNovelRole(**unr_in.model_dump())
    session.add(urn_orm)
    await session.flush()
    await session.refresh(urn_orm)
    return urn_orm


async def get_role_by_name(
    session: AsyncSession,
    name: str,
):
    stmt = select(Role).where(Role.name == name)  # type: ignore
    role = await session.scalar(stmt)
    return role


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
            Role.id == UserNovelRole.role_id,
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


async def get_unrs_by_user_and_novel(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
):
    stmt = select(UserNovelRole).where(
        and_(
            UserNovelRole.user_id == user_id,
            UserNovelRole.novel_id == novel_id,
        )
    )
    unr = await session.scalars(stmt)
    return unr.all()


async def get_roles_id_from_unr_by_user_and_novel(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
):
    stmt = (
        select(UserNovelRole.role_id)
        .select_from(UserNovelRole)
        .where(
            and_(
                UserNovelRole.user_id == user_id,
                UserNovelRole.novel_id == novel_id,
            ),
        )
    )

    result = await session.execute(stmt)

    return result.scalars().all()
