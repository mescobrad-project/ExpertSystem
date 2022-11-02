from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.models._base import Base, GUID


class ModuleModel(Base):
    __tablename__ = "modules"

    category_id = Column(GUID(), ForeignKey("module_categories.id"), index=True)
    code = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    task = Column(String, nullable=False, index=True)
    instructions = Column(JSON, nullable=True)

    category = relationship("ModuleCategoryModel", back_populates="modules")
