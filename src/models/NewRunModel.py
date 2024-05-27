from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewRunModel(Base):
    __tablename__ = "new_runs"

    title: Mapped[str] = mapped_column(String, nullable=True, index=True)
    notes: Mapped[str] = mapped_column(String, nullable=True)
    workflow_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    is_part_of_other: Mapped[bool] = mapped_column(
        Boolean, nullable=True, default=False
    )
    json_representation: Mapped[any] = mapped_column(
        JSON, nullable=True, default=lambda: {}
    )
    step: Mapped[str] = mapped_column(String, nullable=True, index=True)
    action: Mapped[str] = mapped_column(String, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=True, index=True)
    ws_id: Mapped[int] = mapped_column(Boolean, nullable=True, default=False)
