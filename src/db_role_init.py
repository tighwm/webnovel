from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from enums import Resource, Action, RoleNames
from core.database.models import Permission, Role


async def init_permissions(session: AsyncSession):
    permissions_data = [
        {
            "name": "novel.create",
            "resource": Resource.NOVEL.value,
            "action": Action.CREATE.value,
        },
        {
            "name": "novel.read",
            "resource": Resource.NOVEL.value,
            "action": Action.READ.value,
        },
        {
            "name": "novel.edit",
            "resource": Resource.NOVEL.value,
            "action": Action.EDIT.value,
        },
        {
            "name": "novel.delete",
            "resource": Resource.NOVEL.value,
            "action": Action.DELETE.value,
        },
    ]

    for perm_data in permissions_data:
        result = await session.execute(
            select(Permission).where(Permission.name == perm_data["name"])  # type: ignore
        )
        existing_permission = result.scalar_one_or_none()

        if not existing_permission:
            permission = Permission(**perm_data)
            session.add(permission)

    await session.commit()


async def init_roles(session: AsyncSession):
    await init_permissions(session)

    result = await session.execute(select(Permission))
    permissions = {perm.name: perm for perm in result.scalars().all()}

    roles_config = {
        RoleNames.AUTHOR.value: {
            "description": "Автор новеллы с полными правами на свои произведения",
            "permissions": [
                "novel.create",
                "novel.read",
                "novel.edit",
                "novel.delete",
                "novel.publish",
            ],
        },
        RoleNames.READER.value: {
            "description": "Читатель с базовыми правами",
            "permissions": [
                "novel.read",
            ],
        },
    }

    for role_name, config in roles_config.items():
        result = await session.execute(
            select(Role)
            .options(selectinload(Role.permissions))
            .where(Role.name == role_name)
        )
        existing_role = result.scalar_one_or_none()

        if not existing_role:
            role = Role(name=role_name, description=config["description"])

            role_permissions = []
            for perm_name in config["permissions"]:
                if perm_name in permissions:
                    role_permissions.append(permissions[perm_name])

            role.permissions = role_permissions
            session.add(role)

    await session.commit()
