from fastapi import APIRouter

from api.v1.views.auth import router as auth_router
from api.v1.views.user import router as user_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(user_router)
