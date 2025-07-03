from typing import Annotated

from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.services import users
from api.v1.schemas.user import UserRead
from api.v1.utils import oauth2_schema
from core.database.models import db_helper


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    "/{user_id}/",
    response_model=UserRead,
)
async def get_user_by_id(
    user_id: Annotated[
        int,
        Path(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    user = await users.get_user(user_id=user_id, session=session)
    return user


@router.get(
    "/me/",
    response_model=UserRead,
)
async def get_me(
    access_token: Annotated[
        str,
        Depends(oauth2_schema),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await users.get_me_by_token(access_token, session)
