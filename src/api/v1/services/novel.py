from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud import sqlalchemy_novel as novel_crud
from api.v1.crud import sqlalchemy_usernovelrole as unr_crud
from api.v1.schemas.novel import NovelCreate, NovelRead
from api.v1.schemas.usernovelrole import UserNovelRoleCreate
from core.database.models import User


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
    unr = await unr_crud.create(session, unr_create)
    return NovelRead.model_validate(novel)
