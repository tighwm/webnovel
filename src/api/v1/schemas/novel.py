from pydantic import BaseModel, ConfigDict


class NovelBase(BaseModel):
    title: str
    description: str
    author_id: int


class NovelCreate(NovelBase):
    pass


class NovelUpdate(NovelBase):
    pass


class NovelPartial(NovelUpdate):
    title: str | None = None
    description: str | None = None
    author_id: int | None = None


class NovelRead(NovelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
