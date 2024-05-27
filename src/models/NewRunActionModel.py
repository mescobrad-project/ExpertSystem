from sqlalchemy import Boolean, Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseNewRunActionModel(Base):
    __tablename__ = "new_run_actions"

    action_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    action_type: Mapped[str] = mapped_column(String, nullable=True, index=True)
    input: Mapped[str] = mapped_column(String, nullable=True, index=True)
    value: Mapped[str] = mapped_column(String, nullable=True, index=True)
    status: Mapped[str] = mapped_column(String, nullable=True, index=True)
    ws_id: Mapped[int] = mapped_column(Integer, nullable=True, default=False)
    run_id: Mapped[str] = mapped_column(String, nullable=True, default=False)
