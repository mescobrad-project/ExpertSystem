from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ._base import PlatformBase


class BasePlatformWorkspaceModel(PlatformBase):
    __tablename__ = "mcb_workspaces"

    ws_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, primary_key=True
    )
    ws_name: Mapped[str] = mapped_column(String, nullable=True)
    ws_description: Mapped[str] = mapped_column(String, nullable=True)
    ws_type: Mapped[str] = mapped_column(String, nullable=True)
    ws_owner: Mapped[str] = mapped_column(String, nullable=True)
    ws_status: Mapped[str] = mapped_column(String, nullable=True)
    ws_role: Mapped[str] = mapped_column(String, nullable=True)
    ws_created_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), nullable=True
    )
