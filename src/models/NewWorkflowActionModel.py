from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewWorkflowActionModel(Base):
    __tablename__ = "new_workflow_actions"

    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True, index=False)
    workflow_step_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    is_conditional: Mapped[bool] = mapped_column(Boolean, nullable=True, index = False)
    action: Mapped[str] = mapped_column(String, nullable=False, index=False)
    weight_to_true: Mapped[int] = mapped_column(Integer, nullable=True, index = False)
    ws_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
