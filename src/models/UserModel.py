from sqlalchemy import String, JSON, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseUserModel(Base):
    __tablename__ = "users"

    sub: Mapped[str] = mapped_column(String, nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String, nullable=False, index=True)
    info: Mapped[any] = mapped_column(JSON, nullable=True, default=lambda: {})
    permission: Mapped[any] = mapped_column(JSON, nullable=True, default=lambda: {})
    session: Mapped[any] = mapped_column(JSON, nullable=True, default=lambda: {})
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


Index("ix_expert_system_users_sub_provider", BaseUserModel.sub, BaseUserModel.provider)
