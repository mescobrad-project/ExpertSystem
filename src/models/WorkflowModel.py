from sqlalchemy import String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.config import DB_SCHEMA
from ._base import Base, GUID


class BaseWorkflowModel(Base):
    __tablename__ = "workflows"

    category_id: Mapped[GUID] = mapped_column(
        GUID(),
        ForeignKey(f"{DB_SCHEMA}.workflow_categories.id"),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    tasks: Mapped[any] = mapped_column(JSON, nullable=True)
    stores: Mapped[any] = mapped_column(JSON, nullable=True)
    raw_diagram_data: Mapped[any] = mapped_column(JSON, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
