from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base


# Shared properties
class WorkflowBase(Base):
    name: str
    description: str | None = None
    tasks: dict | None = None


# Properties to receive on obj creation
class WorkflowCreate(WorkflowBase):
    pass


# Properties to receive on obj update
class WorkflowUpdate(WorkflowBase):
    pass


# Properties shared by models stored in DB
class WorkflowInDBBase(WorkflowBase):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str | None = None
    tasks: dict | None = None

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
