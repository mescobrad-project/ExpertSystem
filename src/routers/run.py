from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user
from src.schemas.RequestBodySchema import TaskMetadataBodyParameter
from src.schemas.RunSchema import Run, RunNameUpdate

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.post("/workflow/{workflow_id}", response_model=Run)
def run_workflow(*, db: Session = Depends(get_db), workflow_id: UUID):
    """
    Initiate a workflow process
    """
    return RunController.initialize(db=db, workflow_id=workflow_id)


@router.get("/{run_id}", response_model=Run)
def read_run(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
) -> Any:
    """
    Get specific workflow run by ID.
    """
    return RunController.read(db=db, resource_id=run_id, criteria={"deleted_at": None})


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
def show_next_task(*, db: Session = Depends(get_db), run_id: UUID) -> Any:
    """
    Retrieve running instance and return next task(s).
    """
    return RunController.get_next_task(db, run_id)


@router.get("/{run_id}/stores/dataobject")
def get_dataobjects_from_stored_data(
    *, db: Session = Depends(get_db), run_id: UUID
) -> Any:
    """
    Get all data object references mined from stored data.
    """
    return RunController.get_dataobjects_from_stored_data(db, run_id)


@router.get("/{run_id}/step/{step_id}")
def run_specific_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Initiate next step (specific task).
    """
    return RunController.run_specific_task(db, run_id, step_id)


@router.patch("/{run_id}/step/{step_id}/exclusive/{next_step_id}")
def select_next_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID, next_step_id: UUID
) -> Any:
    """
    Select the next task while on Exclusive Gateway
    """
    return RunController.select_next_task(db, run_id, step_id, next_step_id)


@router.patch("/{run_id}/step/{step_id}/parallel/{next_step_id}")
def init_parallel_gateway(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID, next_step_id: UUID
) -> Any:
    """
    Initalize a Parallel Gateway by selecting next task in waiting queue.
    """
    return RunController.init_parallel_gateway(db, run_id, step_id, next_step_id)


@router.patch("/{run_id}/step/{step_id}/task/exec")
def exec_script_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Execute a script task.
    """
    return RunController.exec_script_task(db, run_id, step_id)


@router.patch("/{run_id}/step/{step_id}/task/send")
def send_task(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    step_id: UUID,
    data: dict = {},
) -> Any:
    """
    Send a remote background task.
    """
    return RunController.send_task(db, run_id, step_id, data)


@router.patch("/{run_id}/step/{step_id}/task/receive")
def receive_task(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    step_id: UUID,
    data: dict = {},
) -> Any:
    """
    Send a remote background task.
    """
    return RunController.receive_task(db, run_id, step_id, data.get("metadata"))


@router.patch("/{run_id}/step/{step_id}/task/complete")
def complete_task(
    *,
    db: Session = Depends(get_db),
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
    return RunController.complete_task(db, run_id, step_id, metadata)


@router.patch("/{run_id}/step/{step_id}/event")
def exec_event_task_actions(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Execute the actions of an event task.
    """
    return RunController.exec_event_task_actions(db, run_id, step_id)


@router.get("/{run_id}/step/{step_id}/ping")
def ping_task_status(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Get the status of specific task.
    """
    return RunController.ping_task_status(db, run_id, step_id)
