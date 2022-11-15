from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class ModuleCategoryBase(FormBase):
    pass


# Properties to receive on obj creation
class ModuleCategoryCreate(ModuleCategoryBase):
    code: str
    name: str


# Properties to receive on obj update
class ModuleCategoryUpdate(ModuleCategoryBase):
    code: str | None = None
    name: str | None = None


# Properties shared by models stored in DB
class ModuleCategoryInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str
    code: str

    class Config:
        orm_mode = True


# Properties to return to client
class ModuleCategory(ModuleCategoryInDBBase):
    pass


# Properties stored in DB
class ModuleCategoryInDB(ModuleCategoryInDBBase):
    pass
