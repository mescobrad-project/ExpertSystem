from sqlalchemy import Column, ForeignKey, String, Index, Text
from sqlalchemy.orm import relationship

from src.models._base import Base, GUID, to_tsvector_ix
from src.config import DB_SCHEMA


class FileModel(Base):
    __tablename__ = "files"

    user_id = Column(GUID(), ForeignKey(f"{DB_SCHEMA}.users.id"), index=True)
    name = Column(String, nullable=True)
    bucket_name = Column(String, nullable=True)
    object_name = Column(String, nullable=True)

    __ts_vector__ = to_tsvector_ix("name", "bucket_name", "object_name")

    user = relationship("UserModel", back_populates="files")

    def __repr__(self):
        return f"file({self.name})"


Index(
    "ix_expert_system_files___ts_vector__",
    FileModel.__ts_vector__,
    postgresql_using="gin",
)
