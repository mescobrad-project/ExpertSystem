from sqlalchemy import Column, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base


class Run(Base):
    __tablename__ = "runs"

    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    state = Column(JSON)
    steps = Column(JSON)
    queue = Column(JSON)

    workflow = relationship("Workflow", back_populates="runs")
