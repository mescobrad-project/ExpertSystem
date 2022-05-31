from sqlalchemy import Column, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base, GUID


class Run(Base):
    __tablename__ = "runs"

    workflow_id = Column(GUID(), ForeignKey("workflows.id"), index=True)
    state = Column(JSON, nullable=True)
    steps = Column(JSON, nullable=True)
    queue = Column(JSON, nullable=True)

    workflow = relationship("Workflow", back_populates="runs")
