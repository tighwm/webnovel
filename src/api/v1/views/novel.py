from fastapi import APIRouter

from api.v1.schemas.novel import NovelRead, NovelCreate

router = APIRouter(
    prefix="/novel/",
    tags=["Novel"],
)


@router.post(
    "/",
    response_model=NovelRead,
)
async def handle_create_novel(
    novel_in: NovelCreate,
):
    pass
