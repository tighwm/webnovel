from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.usernovelrole import UserNovelRoleCreate
from core.database.models import UserNovelRole


async def create(
    session: AsyncSession,
    unr_in: UserNovelRoleCreate,
):
    urn_orm = UserNovelRole(**unr_in.model_dump())
    session.add(urn_orm)
    await session.commit()
    await session.refresh(urn_orm)
    return urn_orm
