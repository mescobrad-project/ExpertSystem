from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base, GUID


class WorkflowModel(Base):
    __tablename__ = "workflows"

    category_id = Column(
        GUID(), ForeignKey("workflow_categories.id"), nullable=True, index=True
    )
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    tasks = Column(JSON, nullable=True)
    stores = Column(JSON, nullable=True)
    raw_diagram_data = Column(JSON, nullable=True)

    runs = relationship("RunModel", back_populates="workflow")
    category = relationship("WorkflowCategoryModel", back_populates="workflows")
