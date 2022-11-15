from ._base import BaseCRUD
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate


class _WorkflowRepository(BaseCRUD[WorkflowModel, WorkflowCreate, WorkflowUpdate]):
    pass


WorkflowRepository = _WorkflowRepository(WorkflowModel)
