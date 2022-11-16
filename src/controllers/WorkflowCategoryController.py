from src.repositories.WorkflowCategoryRepository import WorkflowCategoryRepository
from ._base import BaseController


class _WorkflowCategoryController(BaseController):
    pass


WorkflowCategoryController = _WorkflowCategoryController(WorkflowCategoryRepository)
