from sqlalchemy.ext.asyncio import AsyncSession

from api.crud import sqlalchemy_role as role_crud
from enums import Action, Resource
from api.schemas.usernovelrole import UserNovelRoleCreate

from enums import RoleNames


async def assign_unr_to_user(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
    role_name: RoleNames,
):
    role = await role_crud.get_role_by_name(session, role_name.value)

    roles_id = await role_crud.get_roles_id_from_unr_by_user_and_novel(
        session=session,
        user_id=user_id,
        novel_id=novel_id,
    )
    if role.id in roles_id:
        return None

    unr_create = UserNovelRoleCreate(
        user_id=user_id,
        novel_id=novel_id,
        role_id=role.id,
    )
    unr = await role_crud.create_unr(session, unr_create)
    return unr


async def has_permission_to_novel(
    session: AsyncSession,
    user_id: int,
    novel_id: int,
    perm_name: str,
) -> bool:
    perms = await role_crud.get_permissions_for_user_to_novel(
        session=session,
        user_id=user_id,
        novel_id=novel_id,
    )
    if perms is None:
        return False
    return perm_name in perms


async def has_required_permission(
    session: AsyncSession,
    user_id: int,
    target_id: int,
    action: Action,
    resource: Resource,
):
    perm_name = f"{resource.value}.{action.value}"
    if resource == Resource.NOVEL:
        return await has_permission_to_novel(
            session=session,
            user_id=user_id,
            novel_id=target_id,
            perm_name=perm_name,
        )
