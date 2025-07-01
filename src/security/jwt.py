import uuid
from datetime import timedelta, datetime, timezone

import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_path.read_text(),
    algorithms: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithms],
    )
    return decoded


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_min,
    expire_timedelta: timedelta | None = None,
):
    payload = {"token_type": token_type}
    payload.update(token_data)
    return encode_jwt(
        payload=payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(
    sub: str,
):
    payload = {
        "sub": sub,
    }
    return create_jwt(
        token_type="access",
        token_data=payload,
    )


def create_refresh_token(
    jti: uuid.UUID,
    sub: str | None = None,
):
    payload = {
        "sub": sub,
        "jti": str(jti),
    }
    return create_jwt(
        token_type="refresh",
        token_data=payload,
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
