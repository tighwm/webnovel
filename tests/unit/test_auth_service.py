from unittest.mock import MagicMock, Mock, AsyncMock

import pytest

from tests.conftest import mock_session


@pytest.fixture()
def mock_user_crud(monkeypatch):
    mock_crud = MagicMock()
    mock_crud.create = AsyncMock()
    mock_crud.get_by_email = AsyncMock()

    monkeypatch.setattr(
        "api.services.authentication.user_crud",
        mock_crud,
    )
    return mock_crud


@pytest.fixture()
def mock_user_session_crud(monkeypatch):
    mock_crud = MagicMock()
    mock_crud.create = AsyncMock()

    monkeypatch.setattr(
        "api.services.authentication.user_session_crud",
        mock_crud,
    )
    return mock_crud


@pytest.fixture()
def mock_hash_password(monkeypatch):
    mock = Mock()

    monkeypatch.setattr("api.services.authentication.hash_password", mock)
    return mock


@pytest.fixture()
def mock_validate_password(monkeypatch):
    mock = Mock()

    monkeypatch.setattr(
        "api.services.authentication.validate_password",
        mock,
    )
    return mock


@pytest.fixture()
def mock_create_access_token(monkeypatch):
    mock = Mock()

    monkeypatch.setattr(
        "api.services.authentication.create_access_token",
        mock,
    )
    return mock


@pytest.fixture()
def mock_create_refresh_token(monkeypatch):
    mock = Mock()

    monkeypatch.setattr(
        "api.services.authentication.create_refresh_token",
        mock,
    )
    return mock


async def test_register(
    mock_session,
    mock_user_crud,
    mock_hash_password,
):
    from tests.factories import faker
    from api.services.authentication import register
    from api.schemas.user import UserCreate, UserRead

    user_in = UserCreate(
        email=faker.email(),
        name=faker.name(),
        password=faker.password(),
    )
    hashed_password = "supersecret"
    user_in_db = MagicMock()
    user_in_db.id = 1
    user_in_db.email = f"{user_in.email}"
    user_in_db.name = f"{user_in.name}"
    user_in_db.hashed_password = hashed_password
    mock_user_crud.create.return_value = user_in_db
    mock_hash_password.return_value = hashed_password

    result = await register(
        session=mock_session,
        user_in=user_in,
    )
    assert isinstance(result, UserRead)
    assert result.email == user_in.email
    assert result.name == user_in.name
    mock_user_crud.create.assert_called_once()


async def test_register_exception(
    mock_session,
    mock_user_crud,
    mock_hash_password,
):
    from tests.factories import faker
    from api.services.authentication import register
    from api.schemas.user import UserCreate
    from fastapi.exceptions import HTTPException

    user_in = UserCreate(
        email=faker.email(),
        name=faker.name(),
        password=faker.password(),
    )
    hashed_password = "supersecret"
    mock_user_crud.create.return_value = None
    mock_hash_password.return_value = hashed_password

    with pytest.raises(HTTPException):
        await register(
            session=mock_session,
            user_in=user_in,
        )


async def test_login(
    mock_session,
    mock_user_crud,
    mock_user_session_crud,
    mock_validate_password,
    mock_create_access_token,
    mock_create_refresh_token,
):
    from tests.factories import faker
    from api.services.authentication import login
    from api.schemas.tokens import TokenInfo

    email = faker.email()
    password = faker.password()

    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.hashed_password = "supersecret"
    mock_user_crud.get_by_email.return_value = user_mock
    mock_validate_password.return_value = True
    mock_create_access_token.return_value = "access_token"
    mock_create_refresh_token.return_value = "refresh_token"

    result = await login(
        email=email,
        password=password,
        session=mock_session,
    )
    assert isinstance(result, TokenInfo)
    assert result.access == "access_token"
    assert result.refresh == "refresh_token"
    mock_user_crud.get_by_email.assert_called_once_with(
        email=email,
        session=mock_session,
    )
    mock_validate_password.assert_called_once_with(
        password=password,
        hashed_password=user_mock.hashed_password,
    )
    mock_create_access_token.assert_called_once_with(sub=str(user_mock.id))
    mock_create_refresh_token.assert_called_once()
    mock_user_session_crud.create.assert_called_once()
