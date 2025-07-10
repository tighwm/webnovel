from tests.conftest import test_session
from api.crud import sqlalchemy_novel as novel_crud
from api.schemas.novel import NovelCreate
from core.database.models import Novel
from tests.factories import user_factory


async def test_create_novel(test_session, user_factory):
    novel_in = NovelCreate(
        title="Shadow Slave",
        description="The book about little man",
        author_id=user_factory.id,
    )
    result = await novel_crud.create(test_session, novel_in)
    assert result is not None
    assert isinstance(result, Novel)
    fetched = await test_session.get(Novel, result.id)
    assert fetched is not None
    assert fetched.title == result.title
    assert fetched.id == result.id
    assert fetched.description == result.description
    assert fetched.author_id == result.author_id
