from pydantic import BaseModel, ConfigDict


class NovelBase(BaseModel):
    title: str
    description: str


class NovelCreate(NovelBase):
    author_id: int


class NovelUpdate(NovelBase):
    pass


class NovelPartial(NovelUpdate):
    title: str | None = None
    description: str | None = None


class NovelRead(NovelBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author_id: int
