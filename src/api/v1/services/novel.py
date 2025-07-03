from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud import sqlalchemy_novel as novel_crud
from api.v1.crud import sqlalchemy_usernovelrole as unr_crud
from api.v1.schemas.novel import NovelCreate, NovelRead, NovelUpdate
from api.v1.schemas.usernovelrole import UserNovelRoleCreate
from api.v1.utils import exc_404
from core.database.models import User, Novel


async def create_novel(
    novel_in: NovelCreate,
    user: User,
    session: AsyncSession,
):
    novel = await novel_crud.create(session, novel_in)
    unr_create = UserNovelRoleCreate(
        novel_id=novel.id,
        user_id=user.id,
        role_id=1,
    )
    await unr_crud.create(session, unr_create)
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
