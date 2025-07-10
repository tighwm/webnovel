import pytest
from faker import Faker

from core.database.models import User

faker = Faker()


@pytest.fixture()
async def user_factory(test_session, **kwargs):
    user = User(
        email=kwargs.get("email", faker.email()),
        name=kwargs.get("name", faker.name()),
        hashed_password=kwargs.get("hashed_password", faker.password()),
    )
    test_session.add(user)
    await test_session.commit()
    return user
