import uuid

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import UserSession
from api.v1.schemas.user_session import UserSessionBase, UserSessionSchema


async def create(
    session: AsyncSession,
    user_session_in: UserSessionBase,
):
    token_orm = UserSession(**user_session_in.model_dump())
    session.add(token_orm)
    await session.commit()
    return token_orm


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
    await session.commit()
