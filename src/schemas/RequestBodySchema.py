from pydantic import BaseModel, Field


class BpmnDataObject(BaseModel):
    bucket_name: str
    object_name: str
    group_name: str | None = None


class BpmnDataStore(BaseModel):
    table: str
    catalog: str
    name: str
    schema_: str = Field("", alias="schema")


# Used to model the request body params of task complete route
class TaskMetadataBodyParameter(BaseModel):
    store: dict[str, dict[str, list[BpmnDataObject] | list[BpmnDataStore] | list]] = {}
    variables: dict[str, list[dict]] | None = {}
    error: str | None = None


# Used to model the request body params of task complete route
class ScriptTaskCompleteParams(BaseModel):
    data: dict[str, list[BpmnDataObject] | list[BpmnDataStore]] = {}
    ws_id: int
    error: str | None = None


class CallActivityParams(BaseModel):
    parent_workflow_id: str
    workflow_id: str
    run_id: str = ""
    name: str = ""
    settings: dict = {}
