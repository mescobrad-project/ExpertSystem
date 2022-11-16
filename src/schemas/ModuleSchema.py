from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class ModuleBase(FormBase):
    name: str | None = None
    task: str | None = None
    instructions: dict = {}


# Properties to receive on obj creation
class ModuleCreate(ModuleBase):
    code: str
    category_id: UUID


# Properties to receive on obj update
class ModuleUpdate(ModuleBase):
    code: str = None
    category_id: UUID = None


# Properties shared by models stored in DB
class ModuleInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    category_id: UUID
    code: str
    name: str
    task: str
    instructions: dict

    class Config:
        orm_mode = True


# Properties to return to client
class Module(ModuleInDBBase):
    pass


# Properties stored in DB
class ModuleInDB(ModuleInDBBase):
    pass
