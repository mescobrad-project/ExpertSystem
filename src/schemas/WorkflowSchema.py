from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class WorkflowBase(FormBase):
    description: str | None = None
    tasks: dict | None = None
    stores: dict | None = None
    raw_diagram_data: dict | None = None


# Properties to receive on obj creation
class WorkflowCreate(WorkflowBase):
    name: str
    category_id: UUID


# Properties to receive on obj update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    category_id: UUID
    name: str
    description: str | None = None
    tasks: dict | None = None
    stores: dict | None = None
    raw_diagram_data: dict | None = None

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
