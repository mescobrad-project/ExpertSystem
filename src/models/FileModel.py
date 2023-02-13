from sqlalchemy import ForeignKey, String, Index, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.config import DB_SCHEMA
from ._base import Base, GUID, to_tsvector_ix


class BaseFileModel(Base):
    __tablename__ = "files"

    user_id: Mapped[GUID] = mapped_column(
        GUID(), ForeignKey(f"{DB_SCHEMA}.users.id"), index=True
    )
    name: Mapped[String] = mapped_column(String, nullable=True)
    bucket_name: Mapped[String] = mapped_column(String, nullable=True)
    object_name: Mapped[String] = mapped_column(String, nullable=True)

    __ts_vector__ = to_tsvector_ix("name", "bucket_name", "object_name")

    def __repr__(self):
        return f"file({self.name})"


Index(
    "ix_expert_system_files___ts_vector__",
    BaseFileModel.__ts_vector__,
    postgresql_using="gin",
)
