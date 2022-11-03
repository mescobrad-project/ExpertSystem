from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models._base import Base


class WorkflowCategoryModel(Base):
    __tablename__ = "workflow_categories"

    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)

    workflows = relationship("WorkflowModel", back_populates="category")
