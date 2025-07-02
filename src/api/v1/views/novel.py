from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.novel import NovelRead, NovelCreate
from api.v1.utils import get_current_user_by_token
from api.v1.services import novel as novel_serv
from core.database.models import db_helper


router = APIRouter(
    prefix="/novel",
    tags=["Novel"],
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


@router.post(
    "/",
    response_model=NovelRead,
)
async def handle_create(
    novel_in: NovelCreate,
    access_token: Annotated[
        str,
        Depends(oauth2_schema),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user = await get_current_user_by_token(access_token, session)
    return await novel_serv.create_novel(novel_in, user, session)
