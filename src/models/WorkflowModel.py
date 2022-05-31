from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String, nullable=True)
    tasks = Column(JSON, nullable=True)

    runs = relationship("Run", back_populates="workflow")
