from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class FileBase(FormBase):
    name: str | None = None
    ws_id: int | None = None


# Properties to receive on obj creation
class FileCreate(FileBase):
    user_id: UUID
    bucket_name: str
    object_name: str


# Properties to receive on obj update
class FileUpdate(FileBase):
    user_id: UUID = None
    bucket_name: str | None = None
    object_name: str | None = None


# Properties shared by models stored in DB
class FileInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    user_id: UUID
    name: str | None = None
    bucket_name: str
    object_name: str
    ws_id: int = None

    class Config:
        orm_mode = True


# Properties to return to client
class File(FileInDBBase):
    pass


# Properties to return to client
class FileSearch(Base):
    name: str | None = None
    bucket_name: str
    object_name: str

    class Config:
        orm_mode = True


# Properties stored in DB
class FileInDB(FileInDBBase):
    pass
