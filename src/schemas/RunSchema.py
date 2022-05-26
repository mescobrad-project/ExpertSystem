from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base


class Run(Base):
    id: UUID = Field(default_factory=uuid4)
    workflow_id: UUID
    state: dict
    steps: dict
    queue: dict

    class Config:
        orm_mode = True
