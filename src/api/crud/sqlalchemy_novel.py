from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Novel
from api.schemas.novel import NovelCreate, NovelPartial, NovelUpdate


async def create(
    session: AsyncSession,
    novel_in: NovelCreate,
) -> Novel:
    novel = Novel(**novel_in.model_dump())
    session.add(novel)
    await session.flush()
    await session.refresh(novel)
    return novel


async def get_novel_by_id(
    session: AsyncSession,
    novel_id: int,
) -> Novel | None:
    return await session.get(Novel, novel_id)


async def update_novel(
    session: AsyncSession,
    novel: Novel,
    novel_in: NovelUpdate | NovelPartial,
    partial: bool = False,
):
    for name, value in novel_in.model_dump(exclude_unset=partial).items():
        setattr(novel, name, value)
    await session.flush()
    return novel
