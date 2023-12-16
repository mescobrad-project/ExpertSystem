from sqlalchemy import String, Index, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from ._base import Base, to_tsvector_ix


class BaseFileModel(Base):
    __tablename__ = "files"

    name: Mapped[String] = mapped_column(String, nullable=True)
    search: Mapped[Text] = mapped_column(Text, nullable=True)
    info: Mapped[any] = mapped_column(JSON, nullable=True)

    __ts_vector__ = to_tsvector_ix("name", "search")

    def __repr__(self):
        return f"file({self.name})"


Index(
    "ix_expert_system_files___ts_vector__",
    BaseFileModel.__ts_vector__,
    postgresql_using="gin",
)
