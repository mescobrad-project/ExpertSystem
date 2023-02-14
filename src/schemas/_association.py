from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


class FeatureBase(FormBase):
    name: str | None = None
    mapi_id: str | None = None
    info: dict | None = None
    variables: list["VariableBase"] | list | None = None


class VariableBase(FormBase):
    name: str | None = None
    mapi_id: str | None = None
    info: dict | None = None
    features: list["FeatureBase"] | list | None = None


# Properties shared by models stored in DB
class FeatureInDBBaseWithoutRelationship(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: dict | None = None


# Properties shared by models stored in DB
class FeatureInDBBase(FeatureInDBBaseWithoutRelationship):
    variables: list["VariableInDBBaseWithoutRelationship"] | list | None = None

    class Config:
        orm_mode = True


class VariableInDBBaseWithoutRelationship(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: dict | None = None


class VariableInDBBase(VariableInDBBaseWithoutRelationship):
    features: list["FeatureInDBBaseWithoutRelationship"] | list | None = None

    class Config:
        orm_mode = True


FeatureInDBBase.update_forward_refs()
VariableInDBBase.update_forward_refs()
FeatureBase.update_forward_refs()
VariableBase.update_forward_refs()
