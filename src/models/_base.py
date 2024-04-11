from sqlalchemy import DateTime, func, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID as SAUUID
from uuid import uuid4, UUID
from src.config import DB_PLATFORM_SCHEMA, DB_SCHEMA
from src.database import Base as ModelBase


def to_tsvector_ix(*columns):
    s = " || ' ' || ".join(columns)
    return func.to_tsvector("english", text(s))


class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """

    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(SAUUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, UUID):
                return "%.32x" % UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, UUID):
                value = UUID(value)
            return value


class Base(ModelBase):
    __abstract__ = True
    __table_args__ = {"schema": DB_SCHEMA}

    id: Mapped[GUID] = mapped_column(
        GUID(), primary_key=True, default=lambda: str(uuid4())
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)


class PlatformBase(ModelBase):
    __abstract__ = True
    __table_args__ = {"schema": DB_PLATFORM_SCHEMA}
