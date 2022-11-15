from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class WorkflowCategoryBase(FormBase):
    pass


# Properties to receive on obj creation
class WorkflowCategoryCreate(WorkflowCategoryBase):
    code: str
    name: str


# Properties to receive on obj update
class WorkflowCategoryUpdate(WorkflowCategoryBase):
    code: str | None = None
    name: str | None = None


# Properties shared by models stored in DB
class WorkflowCategoryInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str
    code: str

    class Config:
        orm_mode = True


# Properties to return to client
class WorkflowCategory(WorkflowCategoryInDBBase):
    pass


# Properties stored in DB
class WorkflowCategoryInDB(WorkflowCategoryInDBBase):
    pass
