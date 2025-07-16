import os
from unittest.mock import AsyncMock

import pytest
import pg8000.native
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

os.environ.update(
    {
        "APP_CONFIG__DB__URL": "postgresql+asyncpg://user:password@localhost:5432/webnovel-test",
    }
)

from core.database.models import Base
from core.config import settings
from db_role_init import SQLAlchemyRolePermDBInit, permissions_data, roles_config


def is_postgres_responsive(host: str, port: int, user: str, password: str, db: str):
    def check():
        try:
            conn = pg8000.connect(
                user=user,
                host=host,
                port=port,
                password=password,
                database=db,
            )
            conn.close()
            return True
        except Exception:
            return False

    return check


@pytest.fixture(scope="session")
async def wait_for_postgres(docker_services):

    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=1.0,
        check=is_postgres_responsive(
            user="user",
            host="localhost",
            port=5432,
            password="password",
            db="webnovel-test",
        ),
    )


@pytest.fixture(scope="session")
async def test_engine(wait_for_postgres):
    engine = create_async_engine(
        url=str(settings.db.url),
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def roles_init(test_engine):
    session_getter = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    async with session_getter() as test_session:
        roles_init = SQLAlchemyRolePermDBInit(test_session)
        await roles_init.init(perm_data=permissions_data, roles_data=roles_config)


@pytest.fixture(scope="session")
def session_maker(test_engine):
    session_maker = async_sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
    return session_maker


@pytest.fixture()
async def test_session(session_maker):
    async with session_maker() as session:
        yield session
        await session.commit()
@pytest.fixture()
def mock_session():
    return AsyncMock()
