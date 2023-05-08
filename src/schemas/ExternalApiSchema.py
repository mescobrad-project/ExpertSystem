from uuid import UUID
from pydantic import BaseModel


class DataAnalyticsMetadataSchema(BaseModel):
    files: list[list[str]]


# Used to model the request input params of Data Analytics POST fn
class DataAnalyticsInput(BaseModel):
    workflow_id: str | UUID
    run_id: str | UUID
    step_id: str | UUID
    datalake: dict
    trino: dict | None = None
    function: str
    metadata: DataAnalyticsMetadataSchema
