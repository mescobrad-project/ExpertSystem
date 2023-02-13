from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseWorkflowCategoryModel(Base):
    __tablename__ = "workflow_categories"

    code: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
