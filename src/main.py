from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.database.models import db_helper
from core.config import settings

from db_role_init import init_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    session_generator = db_helper.session_getter()
    session = await anext(session_generator)
    await init_roles(session)
    try:
        await anext(session_generator)
    except StopAsyncIteration:
        await session.close()
    del session
    del session_generator
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
