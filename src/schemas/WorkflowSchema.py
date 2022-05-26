from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base


class Workflow(Base):
    id: UUID = Field(default_factory=uuid4)
    name: str
    description: str
    tasks: dict

    class Config:
        orm_mode = True
