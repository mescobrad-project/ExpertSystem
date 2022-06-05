from pydantic import BaseModel, validator
from datetime import datetime, timezone


class Base(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None


class FormBase(Base):
    @validator("updated_at")
    def updateddatetime(cls, _):
        return datetime.now(tz=timezone.utc)
