from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.user import UserSaveToDB
from core.database.models import User


async def create(
    session: AsyncSession,
    user_in: UserSaveToDB,
) -> User:
    user_orm = User(**user_in.model_dump())
    session.add(user_orm)
    await session.commit()
    return user_orm


async def get_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    user_orm = await session.get(User, user_id)
    if user_orm is None:
        return None
    return user_orm  # type: ignore


async def get_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    stmt = select(User).where(User.email == email)  # type: ignore
    user_orm = await session.scalar(stmt)
    if user_orm is None:
        return None
    return user_orm
