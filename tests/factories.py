import pytest
from faker import Faker

from core.database.models import User

faker = Faker()


@pytest.fixture()
async def user_factory(test_session):
    user = User(
        email=faker.email(),
        name=faker.name(),
        hashed_password=faker.password(),
    )
    test_session.add(user)
    await test_session.commit()
    return user
