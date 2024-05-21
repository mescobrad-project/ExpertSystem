from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewRunModel(Base):
    __tablename__ = "new_run"

    title: Mapped[str] = mapped_column(String, nullable=True, index=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    workflow_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    ws_id: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    is_part_of_other: Mapped[bool] = mapped_column(Boolean, nullable=True, default=False)
    json_representation: Mapped[any] = mapped_column(JSON, nullable=True, default=lambda: {})