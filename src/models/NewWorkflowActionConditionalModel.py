from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewWorkflowActionConditionalModel(Base):
    __tablename__ = "new_workflow_action_conditionals"

    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    workflow_action_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    order: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True, index = False)
    variable: Mapped[str] = mapped_column(String, nullable=True, index=False)
    value: Mapped[str] = mapped_column(String, nullable=True, index=False)
    medadata: Mapped[str] = mapped_column(String, nullable=True, index=False)
    