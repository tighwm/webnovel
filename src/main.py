from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.database.models import db_helper
from core.config import settings

from db_role_init import SQLAlchemyRolePermDBInit, roles_config, permissions_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_init = SQLAlchemyRolePermDBInit(db_helper.local_session())
    await db_init.init(
        perm_data=permissions_data,
        roles_data=roles_config,
    )
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
