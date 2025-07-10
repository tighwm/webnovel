from pydantic import BaseModel, ConfigDict


class UserNovelRoleBase(BaseModel):
    user_id: int
    novel_id: int
    role_id: int


class UserNovelRoleCreate(UserNovelRoleBase):
    pass


class UserNovelRoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
