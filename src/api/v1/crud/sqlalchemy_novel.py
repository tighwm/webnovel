from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Novel
from api.v1.schemas.novel import NovelCreate


async def create(
    session: AsyncSession,
    novel_in: NovelCreate,
) -> Novel:
    novel = Novel(**novel_in.model_dump())
    session.add(novel)
    await session.commit()
    await session.refresh(novel)
    return novel
