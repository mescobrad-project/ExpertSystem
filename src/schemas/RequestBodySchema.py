from pydantic import BaseModel


# Used to model the request body params of task complete route
class TaskMetadataBodyParameter(BaseModel):
    objectDataFilePaths: list = []
