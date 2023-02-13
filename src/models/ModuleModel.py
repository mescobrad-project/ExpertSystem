from sqlalchemy import String, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.config import DB_SCHEMA
from ._base import Base, GUID


class BaseModuleModel(Base):
    __tablename__ = "modules"

    category_id: Mapped[GUID] = mapped_column(
        GUID(), ForeignKey(f"{DB_SCHEMA}.module_categories.id"), index=True
    )
    code: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    task: Mapped[str] = mapped_column(String, nullable=False, index=True)
    instructions: Mapped[any] = mapped_column(JSON, nullable=True)
