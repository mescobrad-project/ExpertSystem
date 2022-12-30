from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import BaseModel, Base, FormBase


# Shared properties
class UserBase(FormBase):
    pass


# Properties to receive on obj creation
class UserCreate(UserBase):
    sub: str
    provider: str
    is_active: bool
    info: dict
    permission: dict
    session: dict


# Properties to receive on obj update
class UserUpdate(UserBase):
    is_active: bool | None = None
    info: dict | None = None
    permission: dict | None = None
    session: dict | None = None


# Properties shared by models stored in DB
class UserInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    info: dict
    permission: dict

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties properties stored in DB
class UserInDB(UserInDBBase):
    sub: str
    provider: str
    is_active: bool
    session: dict
