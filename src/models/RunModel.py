from sqlalchemy import Column, ForeignKey, String, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base, GUID


class RunModel(Base):
    __tablename__ = "runs"

    workflow_id = Column(GUID(), ForeignKey("workflows.id"), index=True)
    name = Column(String, nullable=True, index=True)
    state = Column(JSON, nullable=True)
    steps = Column(JSON, nullable=True)
    queue = Column(JSON, nullable=True)

    workflow = relationship("WorkflowModel", back_populates="runs")
