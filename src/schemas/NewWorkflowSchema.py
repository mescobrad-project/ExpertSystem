from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties

class WorkflowActionConditionalBase(FormBase):
    action_id: UUID | None = None
    variable: str | None = None
    value: str | None = None
    weight: float | None = None
    metadata_value: str | None = None
    order: int | None = None
    
class WorkflowActionBase(FormBase):
    name: str | None = None
    description: str | None = None
    step_id: UUID | None = None
    order: int | None = None
    action_type: str | None = None
    is_conditional: bool | None = None
    weight_to_true: float | None = None
    conditions: list[WorkflowActionConditionalBase] | None = None
    
class WorkflowStepBase(FormBase):
    name: str | None = None
    description: str | None = None
    workflow_id: UUID | None = None
    order: int | None = None
    actions: list[WorkflowActionBase] | None = None
    ws_id: int | None = None

class WorkflowBase(FormBase):
    name: str | None = None
    description: str | None = None
    steps: list[WorkflowStepBase] | None = None
    settings: dict | None = None
    json_representation: str | None = None
    is_template: bool = False
    ws_id: int | None = None
    category_id: int | None = None
    is_part_of_other: bool | None = None


# Properties to receive on obj creation
class WorkflowCreate(WorkflowBase):
    name: str
    category_id: UUID


# Properties to receive on obj update
class WorkflowUpdate(WorkflowBase):
    category_id: UUID | None = None


class WorkflowWorkspaceChange(FormBase):
    ws_id: int


# Properties shared by models stored in DB
class WorkflowInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    category_id: UUID | None = None
    name: str
    description: str | None = None
    tasks: dict | None = None
    stores: dict | None = None
    raw_diagram_data: dict | None = None
    is_template: bool = False
    ws_id: int = None

    class Config:
        orm_mode = True


# Properties to return to client
class Workflow(WorkflowInDBBase):
    pass


# Properties properties stored in DB
class WorkflowInDB(WorkflowInDBBase):
    pass
