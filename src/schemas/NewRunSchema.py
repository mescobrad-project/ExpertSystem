from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties


class Run(FormBase):
    id: UUID | None = None
    workflow_id: UUID | None = None
    title: str | None = None
    notes: str | None = None
    ws_id: int | None = None
    is_part_of_other: bool | None = None
    json_representation: str | None = None
    step: str | None = None
    action: str | None = None
    status: str | None = None


class RunAction(FormBase):
    id: UUID | None = None
    action_id: str | None = None
    action_type: str | None = None
    input: str | None = None
    value: str | None = None
    status: str | None = None
    ws_id: int | None = None
