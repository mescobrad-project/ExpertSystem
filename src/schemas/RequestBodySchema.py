from uuid import UUID
from pydantic import BaseModel, Field


class BpmnDataObject(BaseModel):
    bucket_name: str
    object_name: str


class BpmnDataStore(BaseModel):
    table: str
    catalog: str
    name: str
    schema_: str = Field("", alias="schema")


# Used to model the request body params of task complete route
class TaskMetadataBodyParameter(BaseModel):
    store: dict[str, dict[str, list[BpmnDataObject] | list[BpmnDataStore]]] = {}
    error: str | None = None


# Used to model the request body params of task complete route
class ScriptTaskCompleteParams(BaseModel):
    data: dict[str, list[BpmnDataObject] | list[BpmnDataStore]] = {}
    error: str | None = None
