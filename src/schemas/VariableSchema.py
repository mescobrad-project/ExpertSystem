from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class VariableBase(FormBase):
    mapi_id: str | None = None
    info: str | None = None
    features: list[any] | None = None


# Properties to receive on obj creation
class VariableCreate(VariableBase):
    name: str


# Properties to receive on obj update
class VariableUpdate(VariableBase):
    name: str | None = None


# Properties shared by models stored in DB
class VariableInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: str
    features: list[any]

    class Config:
        orm_mode = True


# Properties to return to client
class Variable(VariableInDBBase):
    pass


# Properties stored in DB
class VariableInDB(VariableInDBBase):
    pass
