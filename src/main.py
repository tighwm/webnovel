import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.database.models import db_helper
from core.config import settings

from db_role_init import SQLAlchemyRolePermDBInit, roles_config, permissions_data

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.debug("Start initialization Role and Permission tables...")
    db_init = SQLAlchemyRolePermDBInit(db_helper.local_session())
    await db_init.init(
        perm_data=permissions_data,
        roles_data=roles_config,
    )
    log.debug("Role and Permission tables initialized.")
    yield
    await db_helper.dispose()


mainapp = FastAPI(
    lifespan=lifespan,
)
mainapp.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:mainapp",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
