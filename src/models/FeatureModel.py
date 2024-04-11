from sqlalchemy import String, JSON
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base


class BaseFeatureModel(Base):
    __tablename__ = "features"

    name: Mapped[str] = mapped_column(String, nullable=True, index=True)
    mapi_id: Mapped[str] = mapped_column(String, nullable=True, index=True)
    info: Mapped[any] = mapped_column(JSON, nullable=True, default=lambda: {})
