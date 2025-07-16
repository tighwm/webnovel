from unittest.mock import MagicMock, Mock, AsyncMock

import pytest

from tests.conftest import mock_session


@pytest.fixture()
def mock_user_crud(monkeypatch):
    mock_crud = MagicMock()
    mock_crud.create = AsyncMock()

    monkeypatch.setattr("api.services.authentication.user_crud", mock_crud)
    return mock_crud


@pytest.fixture()
def mock_hash_password(monkeypatch):
    mock = Mock()

    monkeypatch.setattr("api.services.authentication.hash_password", mock)
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
