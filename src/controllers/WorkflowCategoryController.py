from ._base import CRUDBase
from src.models._all import WorkflowCategoryModel
from src.schemas.WorkflowCategorySchema import (
    WorkflowCategoryCreate,
    WorkflowCategoryUpdate,
)


class CRUDWorkflowCategory(
    CRUDBase[WorkflowCategoryModel, WorkflowCategoryCreate, WorkflowCategoryUpdate]
):
    pass


WorkflowCategoryController = CRUDWorkflowCategory(WorkflowCategoryModel)
