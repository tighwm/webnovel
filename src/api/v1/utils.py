from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import BaseModel, EmailStr, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from security.jwt import decode_jwt
from api.v1.crud import sqlalchemy_user as user_crud


oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")


def exc_401(message: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": message,
        },
    )


def validate_token(
    token: str,
    token_type: str,
):
    try:
        payload: dict = decode_jwt(token=token)
    except InvalidTokenError:
        raise exc_401("Invalid token")
    _token_type = payload.get("token_type")
    if _token_type != token_type:
        raise exc_401("Invalid token type")
    return payload


async def get_current_user_by_token(
    access_token: str,
    session: AsyncSession,
):
    payload = validate_token(
        token=access_token,
        token_type="access",
    )
    sub = payload.get("sub")
    user = await user_crud.get_by_id(session, int(sub))
    return user


class EmailLogin(BaseModel):
    email: EmailStr


def validate_form_data(
    form_data: OAuth2PasswordRequestForm,
):
    exc = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Bad username",
    )
    try:
        login = EmailLogin(email=form_data.username)
    except ValidationError:
        raise exc
    password = form_data.password
    return login.email, password
