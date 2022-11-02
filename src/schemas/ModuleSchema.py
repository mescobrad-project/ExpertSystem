from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class ModuleBase(FormBase):
    name: str
    task: str
    instructions: dict


# Properties to receive on obj creation
class ModuleCreate(ModuleBase):
    code: str
    workflow_id: UUID


# Properties to receive on obj update
class ModuleUpdate(ModuleBase):
    pass


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
