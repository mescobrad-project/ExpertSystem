from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models._base import Base


class ModuleCategoryModel(Base):
    __tablename__ = "module_categories"

    code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False, index=True)

    modules = relationship("ModuleModel", back_populates="category")
