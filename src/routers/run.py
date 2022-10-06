from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.controllers.WorkflowEngineController import WorkflowEngineController
from src.database import get_db
from src.controllers.RunController import RunController
from src.schemas.RunSchema import Run

router = APIRouter(
    prefix="/run", tags=["run"], responses={404: {"message": "Not found"}}
)


@router.get("/", response_model=list[Run])
def read_runs(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve worflows with their metadata.
    """
    try:
        runs = RunController.get_multi(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return runs


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
            run.workflows.tasks, run.state, run.steps, run.queue
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    return waiting


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
        workflow = jsonable_encoder(run.workflows)
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
        workflow = jsonable_encoder(run.workflows)
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
        workflow = jsonable_encoder(run.workflows)
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
        workflow = jsonable_encoder(run.workflows)
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
def complete_task(*, db: Session = Depends(get_db), run_id: UUID, step_id: UUID) -> Any:
    """
    Complete a task.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    try:
        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflows)
        response = WorkflowEngineController.task_complete(
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
        workflow = jsonable_encoder(run.workflows)
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
            run.workflows.tasks, run.state, run.steps, run.queue, step_id
        )
    except Exception:
        raise HTTPException(
            status_code=500, detail="Workflow engine faced an unexpected error"
        )

    return response
