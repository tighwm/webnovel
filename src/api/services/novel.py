from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import sqlalchemy_novel as novel_crud
from api.schemas.novel import NovelCreate, NovelRead, NovelUpdate
from api.utils import exc_404
from core.database.models import Novel


async def create_novel(
    novel_in: NovelCreate,
    session: AsyncSession,
):
    novel = await novel_crud.create(session, novel_in)
    return NovelRead.model_validate(novel)


async def get_novel(
    novel_id: int,
    session: AsyncSession,
):
    novel = await novel_crud.get_novel_by_id(
        session=session,
        novel_id=novel_id,
    )
    if novel is None:
        raise exc_404("Novel not found")
    return novel


async def update_novel(
    novel: Novel,
    novel_in: NovelUpdate,
    session: AsyncSession,
):
    novel = await novel_crud.update_novel(session, novel, novel_in)
    return NovelRead.model_validate(novel)
