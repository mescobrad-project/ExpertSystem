from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base


class WorkflowModel(Base):
    __tablename__ = "workflows"

    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    tasks = Column(JSON, nullable=True)
    stores = Column(JSON, nullable=True)
    raw_diagram_data = Column(JSON, nullable=True)

    runs = relationship("RunModel", back_populates="workflow")
