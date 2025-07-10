import uuid
from pydantic import BaseModel, ConfigDict


class UserSessionBase(BaseModel):
    jti: uuid.UUID
    user_id: int


class UserSessionSchema(UserSessionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
