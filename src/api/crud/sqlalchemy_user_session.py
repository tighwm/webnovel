import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import UserSession
from api.schemas.user_session import UserSessionBase, UserSessionSchema


async def create(
    session: AsyncSession,
    user_session_in: UserSessionBase,
):
    user_session_orm = UserSession(**user_session_in.model_dump())
    session.add(user_session_orm)
    await session.flush()
    await session.refresh(user_session_orm)
    return user_session_orm


async def get_by_jti(
    session: AsyncSession,
    jti: uuid.UUID,
):
    stmt = select(UserSession).where(UserSession.jti == jti)  # type: ignore
    user_session = await session.scalar(stmt)
    if user_session is None:
        return None
    return UserSessionSchema.model_validate(user_session)


async def delete_by_jti(
    session: AsyncSession,
    jti: uuid.UUID,
):
    stmt = delete(UserSession).where(UserSession.jti == jti)  # type: ignore
    await session.execute(stmt)
    await session.flush()
