from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.controllers.WorkflowEngineController import WorkflowEngineController
from src.database import get_db
from src.controllers.WorkflowController import WorkflowController
from src.controllers.RunController import RunController
from src.schemas.RequestBodySchema import TaskMetadataBodyParameter
from src.schemas.RunSchema import Run, RunUpdate

router = APIRouter(
    prefix="/run", tags=["run"], responses={404: {"message": "Not found"}}
)


@router.post("/workflow/{workflow_id}", response_model=Run)
def run_workflow(*, db: Session = Depends(get_db), workflow_id: UUID):
    """
    Initiate a workflow process
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    try:
        run = RunController.initialize(db=db, workflow_id=workflow.id)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Run already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Something went wrong")

    try:
        state, steps, queue = WorkflowEngineController.initialize(workflow.tasks)
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    run_in = RunUpdate(state=state, steps=steps, queue=queue)
    run = RunController.update(db=db, db_obj=run, obj_in=run_in)
    return run


@router.get("/{run_id}", response_model=Run)
def read_run(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
) -> Any:
    """
    Get specific workflow run by ID.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    return run


@router.get("/{run_id}/next")
def show_next_task(*, db: Session = Depends(get_db), run_id: UUID) -> Any:
    """
    Retrieve running instance and return next task(s).
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        waiting = WorkflowEngineController.get_waiting_steps(
            run.workflow.tasks, run.state, run.steps, run.queue
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    return waiting


@router.get("/{run_id}/stores/dataobject")
def get_dataobjects_from_stored_data(
    *, db: Session = Depends(get_db), run_id: UUID
) -> Any:
    """
    Get all data object references mined from stored data.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        file_refs = []

        for activity in run.state["data"]:
            for sid, data in activity["data"].items():
                if sid in run.workflow.stores.keys():
                    if run.workflow.stores[sid]["type"] == "DataObject":
                        if "get" in data.keys():
                            file_refs.extend(data["get"])
                        if "set" in data.keys():
                            file_refs.extend(data["set"])

        return file_refs
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )


@router.get("/{run_id}/step/{step_id}")
def run_specific_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Initiate next step (specific task).
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        pending_and_waiting = WorkflowEngineController.run_pending_step(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return pending_and_waiting


@router.patch("/{run_id}/step/{step_id}/exclusive/{next_step_id}")
def select_next_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID, next_step_id: UUID
) -> Any:
    """
    Select the next task while on Exclusive Gateway
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        response = WorkflowEngineController.gateway_exclusive_choice(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
            next_step_id,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return response


@router.patch("/{run_id}/step/{step_id}/parallel/{next_step_id}")
def init_parallel_gateway(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID, next_step_id: UUID
) -> Any:
    """
    Initalize a Parallel Gateway by selecting next task in waiting queue.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        response = WorkflowEngineController.gateway_parallel_choice(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
            next_step_id,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return response


@router.patch("/{run_id}/step/{step_id}/task/exec")
def exec_script_task(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Execute a script task.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        response = WorkflowEngineController.task_exec(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return response


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
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        response = WorkflowEngineController.task_complete(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
            metadata,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return response


@router.patch("/{run_id}/step/{step_id}/event")
def exec_event_task_actions(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Execute the actions of an event task.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        response = WorkflowEngineController.event_actions(
            workflow["tasks"],
            run_in["state"],
            run_in["steps"],
            run_in["queue"],
            step_id,
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    RunController.update(db=db, db_obj=run, obj_in=run_in)

    return response


@router.get("/{run_id}/step/{step_id}/ping")
def ping_task_status(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID
) -> Any:
    """
    Get the status of specific task.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        response = WorkflowEngineController.ping_step_status(
            run.workflow.tasks, run.state, run.steps, run.queue, step_id
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    return response
