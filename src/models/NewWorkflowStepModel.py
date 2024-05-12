from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewWorkflowStepModel(Base):
    __tablename__ = "new_workflow_steps"

    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    