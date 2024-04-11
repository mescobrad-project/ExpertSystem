from sqlalchemy import ForeignKey, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.config import DB_SCHEMA
from ._base import Base, GUID


class BaseRunModel(Base):
    __tablename__ = "runs"

    workflow_id: Mapped[GUID] = mapped_column(
        GUID(), ForeignKey(f"{DB_SCHEMA}.workflows.id"), index=True
    )
    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    state: Mapped[any] = mapped_column(JSON, nullable=True)
    steps: Mapped[any] = mapped_column(JSON, nullable=True)
    queue: Mapped[any] = mapped_column(JSON, nullable=True)
