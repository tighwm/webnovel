from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Cookie,
    Form,
)
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.services import authentication as auth
from api.v1.schemas.user import UserRead, UserCreate
from core.database.models import db_helper

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/register/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def handle_register(
    user_in: UserCreate,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await auth.register(
        user_in=user_in,
        session=session,
    )


@router.post(
    "/login/",
)
async def handle_login(
    response: Response,
    email: Annotated[
        EmailStr,
        Form(),
    ],
    password: Annotated[
        str,
        Form(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    tokens = await auth.login(
        email=email,
        password=password,
        session=session,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh,
        httponly=True,
    )
    return {"access": tokens.access}


@router.post(
    "/refresh/",
)
async def handle_refresh(
    refresh_token: Annotated[
        str,
        Cookie(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    tokens = await auth.refresh(refresh_token, session)
    return {"access": tokens.access}


@router.post(
    "/logout/",
)
async def handle_logout(
    response: Response,
    refresh_token: Annotated[
        str,
        Cookie(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    await auth.logout(refresh_token, session)
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
    )
    return {"success": "true"}
