from sqlalchemy import Column, String, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base


class Workflow(Base):
    __tablename__ = "workflows"

    name = Column(String, unique=True, index=True)
    description = Column(String)
    tasks = Column(JSON)

    runs = relationship("Run", back_populates="workflow")
