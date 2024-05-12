from ._base import BaseCRUD
from src.models._all import WorkflowModel
from src.schemas.NewWorkflowSchema import NewWorkflowCreate, NewWorkflowUpdate


class _NewWorkflowRepository(BaseCRUD):
    pass


WorkflowRepository = _NewWorkflowRepository()
