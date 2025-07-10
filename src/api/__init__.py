from fastapi import APIRouter
from api.views.novel import router as novel_router
from api.views.user import router as user_router
from api.views.auth import router as auth_router

router = APIRouter(prefix="/api")

router.include_router(novel_router)
router.include_router(user_router)
router.include_router(auth_router)
