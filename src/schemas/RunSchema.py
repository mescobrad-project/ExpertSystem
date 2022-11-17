from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import BaseModel, Base, FormBase


# Shared properties
class RunBase(FormBase):
    name: str | None = None


# Properties to receive on obj creation
class RunCreate(RunBase):
    workflow_id: UUID
    state: dict
    steps: list
    queue: list


# Properties to receive on obj update
class RunUpdate(RunBase):
    state: dict | None = None
    steps: list | None = None
    queue: list | None = None


# Properties to receive on obj update
class RunNameUpdate(BaseModel):
    name: str


# Properties shared by models stored in DB
class RunInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    workflow_id: UUID
    state: dict
    steps: list
    queue: list

    class Config:
        orm_mode = True


# Properties to return to client
class Run(RunInDBBase):
    pass


# Properties properties stored in DB
class RunInDB(RunInDBBase):
    pass
