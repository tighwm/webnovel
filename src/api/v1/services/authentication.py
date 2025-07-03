import uuid

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.utils import exc_401, validate_token, exc_422
from security.jwt import create_access_token, create_refresh_token
from api.v1.schemas.user import UserCreate, UserSaveToDB, UserRead
from api.v1.schemas.tokens import TokenInfo
from security.passwords import hash_password, validate_password
from api.v1.schemas.user_session import UserSessionBase
from api.v1.crud import sqlalchemy_user as user_crud
from api.v1.crud import sqlalchemy_user_session as user_session_crud


async def register(
    user_in: UserCreate,
    session: AsyncSession,
) -> UserRead:
    user_data = user_in.model_dump()
    password = user_data.pop("password")
    user_data["hashed_password"] = hash_password(password)
    user_save = UserSaveToDB(**user_data)
    user_db = await user_crud.create(
        user_in=user_save,
        session=session,
    )
    if user_db is None:
        raise exc_422(f"User with {user_save.email} exist")
    return UserRead.model_validate(user_db)


async def login(
    email: EmailStr,
    password: str,
    session: AsyncSession,
) -> TokenInfo:
    user = await user_crud.get_by_email(
        email=email,
        session=session,
    )
    if user is None:
        raise exc_401("Invalid login or password")
    if not validate_password(
        password=password,
        hashed_password=user.hashed_password,
    ):
        raise exc_401("Invalid login or password")

    access_token = create_access_token(sub=str(user.id))
    jti = uuid.uuid4()
    refresh_token = create_refresh_token(sub=str(user.id), jti=jti)
    user_session = UserSessionBase(jti=jti, user_id=user.id)
    await user_session_crud.create(
        session=session,
        user_session_in=user_session,
    )
    return TokenInfo(
        access=access_token,
        refresh=refresh_token,
    )


async def refresh(
    refresh_token: str,
    session: AsyncSession,
) -> TokenInfo:
    payload = validate_token(
        token=refresh_token,
        token_type="refresh",
    )
    jti = uuid.UUID(payload.get("jti"))
    user_session = await user_session_crud.get_by_jti(
        jti=jti,
        session=session,
    )
    if user_session is None:
        raise exc_401("Invalid token")
    sub = payload.get("sub")
    access_token = create_access_token(sub)
    return TokenInfo(access=access_token)


async def logout(
    refresh_token: str,
    session: AsyncSession,
) -> None:
    payload = validate_token(
        token=refresh_token,
        token_type="refresh",
    )
    jti = uuid.UUID(payload.get("jti"))
    await user_session_crud.delete_by_jti(
        jti=jti,
        session=session,
    )
