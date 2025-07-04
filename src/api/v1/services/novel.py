from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud import sqlalchemy_novel as novel_crud
from api.v1.services import role as role_serv
from api.v1.schemas.novel import NovelCreate, NovelRead, NovelUpdate
from api.v1.utils import exc_404
from core.database.models import User, Novel


async def create_novel(
    novel_in: NovelCreate,
    user: User,
    session: AsyncSession,
):
    novel = await novel_crud.create(session, novel_in)
    unr = await role_serv.assign_unr_to_user(
        session=session,
        user_id=user.id,
        novel_id=novel.id,
        role_name="author",
    )
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
