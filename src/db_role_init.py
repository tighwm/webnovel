from abc import ABC, abstractmethod

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from enums import Resource, Action, RoleNames
from core.database.models import Permission, Role

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

roles_config = {
    RoleNames.AUTHOR.value: {
        "description": "Автор новеллы с полными правами на свои произведения",
        "permissions": [
            "novel.create",
            "novel.read",
            "novel.edit",
            "novel.delete",
        ],
    },
    RoleNames.READER.value: {
        "description": "Читатель с базовыми правами",
        "permissions": [
            "novel.read",
        ],
    },
}


class AbstractRolePermDBInit(ABC):

    def __init__(self, session):
        self.session = session

    @abstractmethod
    async def _init_permissions(self, perm_data):
        pass

    @abstractmethod
    async def _close_session(self):
        pass

    @abstractmethod
    async def _init_roles(self, roles_data):
        pass

    @abstractmethod
    async def _commit(self):
        pass

    async def init(self, perm_data, roles_data):
        await self._init_permissions(perm_data)
        await self._init_roles(roles_data)
        await self._commit()
        await self._close_session()


class SQLAlchemyRolePermDBInit(AbstractRolePermDBInit):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

    async def _init_permissions(self, perm_data):
        for perm_data in permissions_data:
            result = await self.session.execute(
                select(Permission).where(Permission.name == perm_data["name"])  # type: ignore
            )
            existing_permission = result.scalar_one_or_none()

            if not existing_permission:
                permission = Permission(**perm_data)
                self.session.add(permission)

        await self.session.flush()

    async def _init_roles(self, roles_data):
        result = await self.session.execute(select(Permission))
        permissions = {perm.name: perm for perm in result.scalars().all()}

        for role_name, config in roles_data.items():
            result = await self.session.execute(
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
                self.session.add(role)

        self.session.flush()

    async def _close_session(self):
        await self.session.close()

    async def _commit(self):
        await self.session.commit()
