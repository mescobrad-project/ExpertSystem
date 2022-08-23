from ._base import CRUDBase
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate
from src.engine.config import (
    START_EVENT,
    END_EVENT,
    EXCLUSIVE_GATEWAY,
    PARALLEL_GATEWAY,
    MANUAL_TASK,
    SCRIPT_TASK,
)


class CRUDWorkflow(CRUDBase[WorkflowModel, WorkflowCreate, WorkflowUpdate]):
    def get_workflow_entity_types(self):
        return {
            "events": [
                START_EVENT,
                END_EVENT,
            ],
            "gateways": [
                EXCLUSIVE_GATEWAY,
                PARALLEL_GATEWAY,
            ],
            "tasks": [
                MANUAL_TASK,
                SCRIPT_TASK,
            ],
        }


WorkflowController = CRUDWorkflow(WorkflowModel)
