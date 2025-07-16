import pytest
from unittest.mock import AsyncMock, MagicMock

from tests.conftest import mock_session


@pytest.fixture()
def mock_role_crud(monkeypatch):
    mock_crud = MagicMock()
    mock_crud.get_role_by_name = AsyncMock()
    mock_crud.get_roles_id_from_unr_by_user_and_novel = AsyncMock()
    mock_crud.create_unr = AsyncMock()
    mock_crud.get_permissions_for_user_to_novel = AsyncMock()

    monkeypatch.setattr("api.services.role.role_crud", mock_crud)
    return mock_crud


async def test_assign_unr_to_user(mock_session, mock_role_crud):
    from api.services.role import assign_unr_to_user
    from enums import RoleNames

    user_id = 123
    novel_id = 321
    role_name = RoleNames.AUTHOR

    mock_role = MagicMock()
    mock_role.id = 1

    mock_unr = MagicMock()
    mock_unr.user_id = user_id
    mock_unr.novel_id = novel_id
    mock_unr.role_id = mock_role.id

    mock_role_crud.get_role_by_name.return_value = mock_role
    mock_role_crud.get_roles_id_from_unr_by_user_and_novel.return_value = []
    mock_role_crud.create_unr.return_value = mock_unr

    result = await assign_unr_to_user(
        mock_session,
        user_id,
        novel_id,
        role_name,
    )

    assert result == mock_unr
    mock_role_crud.get_role_by_name.assert_called_once_with(
        mock_session,
        role_name.value,
    )
    mock_role_crud.get_roles_id_from_unr_by_user_and_novel.assert_called_once_with(
        session=mock_session,
        user_id=user_id,
        novel_id=novel_id,
    )
    mock_role_crud.create_unr.assert_called_once()

    _, create_unr = mock_role_crud.create_unr.call_args.args

    assert create_unr.user_id == user_id
    assert create_unr.role_id == mock_role.id
    assert create_unr.novel_id == novel_id


async def test_has_permission_to_novel(mock_session, mock_role_crud):
    from api.services.role import has_permission_to_novel

    user_id = 123
    novel_id = 321

    mock_role_crud.get_permissions_for_user_to_novel.return_value = (
        "novel.edit",
        "novel.read",
    )

    result = await has_permission_to_novel(
        session=mock_session,
        user_id=user_id,
        novel_id=novel_id,
        perm_name="novel.read",
    )

    assert result is True
    mock_role_crud.get_permissions_for_user_to_novel.assert_called_once_with(
        session=mock_session,
        user_id=user_id,
        novel_id=novel_id,
    )


async def test_has_permission_to_novel_no_permission(mock_session, mock_role_crud):
    from api.services.role import has_permission_to_novel

    user_id = 123
    novel_id = 321

    mock_role_crud.get_permissions_for_user_to_novel.return_value = ("novel.edit",)

    result = await has_permission_to_novel(
        session=mock_session,
        user_id=user_id,
        novel_id=novel_id,
        perm_name="novel.read",
    )

    assert result is False
    mock_role_crud.get_permissions_for_user_to_novel.assert_called_once_with(
        session=mock_session,
        user_id=user_id,
        novel_id=novel_id,
    )
