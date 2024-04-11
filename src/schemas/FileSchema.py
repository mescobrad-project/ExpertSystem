from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class FileBase(FormBase):
    name: str | None = None
    ws_id: int | None = None


# Properties to receive on obj creation
class FileCreate(FileBase):
    search: str
    info: dict


# Properties to receive on obj update
class FileUpdate(FileBase):
    search: str | None = None
    info: dict | None = None


# Properties shared by models stored in DB
class FileInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    search: str
    info: dict
    ws_id: int = None

    class Config:
        orm_mode = True


# Properties to return to client
class File(FileInDBBase):
    pass


# Properties to return to client
class FileSearch(Base):
    name: str | None = None
    info: dict

    class Config:
        orm_mode = True


# Properties stored in DB
class FileInDB(FileInDBBase):
    pass
