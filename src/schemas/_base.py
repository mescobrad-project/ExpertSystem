from pydantic import BaseModel, validator
from datetime import datetime, timezone


class Base(BaseModel):
    created_at: datetime = None
    updated_at: datetime = None
    deleted_at: datetime = None

    @validator("created_at")
    def createdatetime(cls):
        return datetime.now(tz=timezone.utc)

    @validator("updated_at")
    def updatedatetime(cls):
        return datetime.now(tz=timezone.utc)

    @validator("deleted_at")
    def deletedatetime(cls):
        return datetime.now(tz=timezone.utc)
