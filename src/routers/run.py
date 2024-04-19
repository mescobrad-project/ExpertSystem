from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user
from src.dependencies.workspace import validate_workspace
from src.schemas.RequestBodySchema import (
    TaskMetadataBodyParameter,
    CallActivityParams,
)
from src.schemas.RunSchema import Run, RunNameUpdate

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.post("/workflow/{workflow_id}", response_model=Run)
def run_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_id: UUID,
    data: dict = {},
):
    """
    Initiate a workflow process
    """
    return RunController.initialize(
        db=db,
        ws_id=ws_id,
        workflow_id=workflow_id,
        name=data.get("name", ""),
        settings=data.get("settings", {}),
    )


@router.get("/{run_id}", response_model=Run)
def read_run(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
) -> Any:
    """
    Get specific workflow run by ID.
    """
    return RunController.read(
        db=db, resource_id=run_id, criteria={"deleted_at": None, "ws_id": ws_id}
    )


@router.put("/{run_id}", response_model=Run)
def name_a_run(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    props: RunNameUpdate,
) -> Any:
    """
    Name a running instance.
    """
    return RunController.update_name(db=db, resource_id=run_id, name=props.name)


@router.get("/{run_id}/next")
def show_next_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
) -> Any:
    """
    Retrieve running instance and return next task(s).
    """
    return RunController.get_next_task(db, ws_id, run_id)


@router.get("/{run_id}/stores/dataobject")
def get_dataobjects_from_stored_data(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
) -> Any:
    """
    Get all data object references mined from stored data.
    """
    return RunController.get_dataobjects_from_stored_data(db, ws_id, run_id)


@router.get("/{run_id}/stores/datastore")
def get_datastores_from_stored_data(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
) -> Any:
    """
    Get all data object references mined from stored data.
    """
    return RunController.get_datastores_from_stored_data(db, ws_id, run_id)


@router.get("/{run_id}/step/{step_id}")
def run_specific_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
) -> Any:
    """
    Initiate next step (specific task).
    """
    return RunController.run_specific_task(db, ws_id, run_id, step_id)


@router.patch("/{run_id}/step/{step_id}/exclusive/{next_step_id}")
def select_next_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    next_step_id: UUID,
) -> Any:
    """
    Select the next task while on Exclusive Gateway
    """
    return RunController.select_next_task(db, ws_id, run_id, step_id, next_step_id)


@router.patch("/{run_id}/step/{step_id}/parallel/{next_step_id}")
def init_parallel_gateway(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    next_step_id: UUID,
) -> Any:
    """
    Initalize a Parallel Gateway by selecting next task in waiting queue.
    """
    return RunController.init_parallel_gateway(db, ws_id, run_id, step_id, next_step_id)


@router.patch("/{run_id}/step/{step_id}/task/exec")
def exec_script_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    data: dict = {},
) -> Any:
    """
    Execute a script task.
    """
    return RunController.exec_script_task(db, ws_id, run_id, step_id, data)


@router.patch("/{run_id}/step/{step_id}/activity/call")
def exec_call_activity(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    data: CallActivityParams,
) -> Any:
    """
    Execute a nested workflow.
    """
    return RunController.exec_call_activity(db, ws_id, run_id, step_id, data)


@router.patch("/{run_id}/step/{step_id}/task/send")
def send_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    data: dict = {},
) -> Any:
    """
    Send a remote background task.
    """
    return RunController.send_task(db, ws_id, run_id, step_id, data)


@router.patch("/{run_id}/step/{step_id}/task/receive")
def receive_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    data: dict = {},
) -> Any:
    """
    Send a remote background task.
    """
    return RunController.receive_task(db, ws_id, run_id, step_id, data.get("metadata"))


@router.patch("/{run_id}/step/{step_id}/task/complete")
def complete_task(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
    metadata: TaskMetadataBodyParameter | None = None,
) -> Any:
    """
    Complete a task.
    Request body schema is not clear enough.
    Example:
    {
        "store": {
            "store_sid": {
                \<mode>: [
                    \<BpmnDataObject> | \<BpmnDataStore>
                ]
            }
        }
    }
    """
    return RunController.complete_task(db, ws_id, run_id, step_id, metadata)


@router.patch("/{run_id}/step/{step_id}/task/script/complete")
def complete_script_task(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    step_id: UUID,
    data: dict | None = None,
) -> Any:
    """
    Complete a task.
    Request body schema is not clear enough.
    Example:
    {
        "data": {
            [
                \<BpmnDataObject>
            ]
        }
    }
    """
    return RunController.complete_script_task(db, run_id, step_id, data)


@router.patch("/{run_id}/activity/call/complete")
def call_activity_is_completed(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
) -> Any:
    """
    Complete a nested workflow task.
    """
    return RunController.call_activity_is_completed(db, ws_id, run_id)


@router.patch("/{run_id}/step/{step_id}/event")
def exec_event_task_actions(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    step_id: UUID,
) -> Any:
    """
    Execute the actions of an event task.
    """
    return RunController.exec_event_task_actions(db, ws_id, run_id, step_id)


@router.get("/{run_id}/step/{step_id}/ping")
def ping_task_status(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Get the status of s specific task.
    """
    return RunController.ping_task_status(db, run_id, step_id)


@router.get("/{run_id}/step/{step_id}/metadata")
def get_task_metadata(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Get the metadata of a specific task.
    """
    return RunController.get_task_metadata(db, run_id, step_id)


@router.get("/{run_id}/completed/tasks")
def get_completed_tasks(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    run_id: UUID,
    class_name: str | None = None,
    not_in_type: str | None = None,
) -> Any:
    """
    Get previously completed Tasks
    """
    return RunController.get_completed_script_tasks(
        db, ws_id, run_id, class_name=class_name, not_in_type=not_in_type
    )
