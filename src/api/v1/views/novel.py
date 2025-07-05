from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from enums import Action, Resource, RoleNames
from api.v1.schemas.novel import NovelRead, NovelCreate, NovelUpdate
from api.v1.utils import get_current_user_by_token, oauth2_schema, exc_403
from api.v1.services import novel as novel_serv
from api.v1.services import role as role_serv
from api.v1.utils import validate_token
from core.database.models import db_helper


router = APIRouter(
    prefix="/novel",
    tags=["Novel"],
)


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
    novel = await novel_serv.create_novel(novel_in, session)
    unr = await role_serv.assign_unr_to_user(
        session=session,
        user_id=user.id,
        novel_id=novel.id,
        role_name=RoleNames.AUTHOR.value,
    )
    return novel


@router.put(
    "/{novel_id}/",
    response_model=NovelRead,
)
async def handle_update(
    novel_in: NovelUpdate,
    novel_id: int,
    access_token: Annotated[
        str,
        Depends(oauth2_schema),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    payload = validate_token(
        token=access_token,
        token_type="access",
    )
    user_id = int(payload.get("sub"))
    novel = await novel_serv.get_novel(
        novel_id=novel_id,
        session=session,
    )
    if not await role_serv.has_required_permission(
        session=session,
        user_id=user_id,
        target_id=novel_id,
        action=Action.EDIT,
        resource=Resource.NOVEL,
    ):
        raise exc_403("Has no permission")

    return await novel_serv.update_novel(
        novel=novel,
        novel_in=novel_in,
        session=session,
    )
