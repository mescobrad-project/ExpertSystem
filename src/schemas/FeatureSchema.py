from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


# Shared properties
class FeatureBase(FormBase):
    mapi_id: str | None = None
    info: str | None = None
    variables: list[any] | None = None


# Properties to receive on obj creation
class FeatureCreate(FeatureBase):
    name: str


# Properties to receive on obj update
class FeatureUpdate(FeatureBase):
    name: str | None = None


# Properties shared by models stored in DB
class FeatureInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: str
    variables: list[any]

    class Config:
        orm_mode = True


# Properties to return to client
class Feature(FeatureInDBBase):
    pass


# Properties stored in DB
class FeatureInDB(FeatureInDBBase):
    pass
