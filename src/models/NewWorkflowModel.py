from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewWorkflowModel(Base):
    __tablename__ = "new_workflows"

    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    is_template: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_part_of_other: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False
    )
    json_representation: Mapped[any] = mapped_column(
        JSON, nullable=True, default=lambda: {}
    )
