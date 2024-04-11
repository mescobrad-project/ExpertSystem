from ._base import BaseCRUD
from src.models._all import WorkflowCategoryModel
from src.schemas.WorkflowCategorySchema import (
    WorkflowCategoryCreate,
    WorkflowCategoryUpdate,
)


class _WorkflowCategoryRepository(
    BaseCRUD[WorkflowCategoryModel, WorkflowCategoryCreate, WorkflowCategoryUpdate]
):
    pass


WorkflowCategoryRepository = _WorkflowCategoryRepository(WorkflowCategoryModel)
