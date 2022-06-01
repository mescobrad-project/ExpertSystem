from ._base import CRUDBase
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate


class CRUDWorkflow(CRUDBase[WorkflowModel, WorkflowCreate, WorkflowUpdate]):
    pass


WorkflowController = CRUDWorkflow(WorkflowModel)
