from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.utils import validate_token
from api.v1.crud import sqlalchemy_permission as perm_crud


async def has_permission_to_novel(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
    perm_name: str,
) -> bool:
    perms = await perm_crud.get_permissions_for_user_to_novel(
        session=session,
        user_id=user_id,
        novel_id=novel_id,
    )
    if perms is None:
        return False
    return perm_name in perms


async def check_can_edit_novel_by_token(
    session: AsyncSession,
    access_token: str,
    novel_id: int,
):
    payload = validate_token(
        token=access_token,
        token_type="access",
    )
    user_id = int(payload.get("sub"))

    return await has_permission_to_novel(
        session=session,
        user_id=user_id,
        novel_id=novel_id,
        perm_name="novel.edit",
    )
