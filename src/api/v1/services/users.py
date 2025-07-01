from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud import sqlalchemy_user as user_crud
from api.v1.schemas.user import UserRead


def exc_404(
    message: str,
):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": message},
    )


async def get_user(
    user_id: int,
    session: AsyncSession,
) -> UserRead:
    user = await user_crud.get_by_id(
        user_id=user_id,
        session=session,
    )
    if user is None:
        raise exc_404("User not found")

    return UserRead.model_validate(user)
