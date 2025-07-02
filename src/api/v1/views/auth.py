from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
    Response,
    Cookie,
)
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.services import authentication as auth
from api.v1.schemas.user import UserRead, UserCreate
from api.v1.utils import validate_form_data
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
    "/token/",
)
async def handle_login(
    response: Response,
    form_data: Annotated[
        OAuth2PasswordRequestForm,
        Depends(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    email, password = validate_form_data(form_data)
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
    return {
        "access_token": tokens.access,
        "token_type": "bearer",
    }


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
    return {
        "access": tokens.access,
        "token_type": "bearer",
    }


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
