from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserSaveToDB(UserBase):
    hashed_password: str


class UserUpdate(UserCreate):
    pass


class UserPartial(UserUpdate):
    name: str | None = None
    password: str | None = None
    email: EmailStr | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
