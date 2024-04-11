from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ._base import PlatformBase


class BasePlatformUserDefaultWorkspaceModel(PlatformBase):
    __tablename__ = "mcb_user_default_workspace"

    usr_def_ws_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True, primary_key=True
    )
    user_name: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String, nullable=True)
    updated_on: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False), nullable=True
    )
