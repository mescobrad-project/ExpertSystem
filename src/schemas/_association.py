from pydantic import Field
from uuid import UUID, uuid4
from src.schemas._base import Base, FormBase


class FeatureBase(FormBase):
    name: str | None = None
    mapi_id: str | None = None
    info: str | None = {}
    variables: list["VariableBase"] | None = []


class VariableBase(FormBase):
    name: str | None = None
    mapi_id: str | None = None
    info: str | None = {}
    features: list["FeatureBase"] | None = []


# Properties shared by models stored in DB
class FeatureInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: str | None = {}
    variables: list["VariableInDBBase"] | None = []

    class Config:
        orm_mode = True


class VariableInDBBase(Base):
    id: UUID = Field(default_factory=lambda: uuid4().hex)
    name: str | None = None
    mapi_id: str | None = None
    info: str | None = {}
    features: list["FeatureInDBBase"] | None = []

    class Config:
        orm_mode = True
