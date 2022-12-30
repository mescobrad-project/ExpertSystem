from sqlalchemy import Column, String, JSON, Boolean, Index
from src.models._base import Base


class UserModel(Base):
    __tablename__ = "users"

    sub = Column(String, nullable=False, index=True)
    provider = Column(String, nullable=False, index=True)
    info = Column(JSON, nullable=True)
    permission = Column(JSON, nullable=True)
    session = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True, index=True)


Index("ix_expert_system_users_sub_provider", UserModel.sub, UserModel.provider)
