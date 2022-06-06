from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.controllers.RunController import RunController
from src.schemas.RunSchema import Run, RunCreate, RunUpdate

router = APIRouter(
    prefix="/run", tags=["run"], responses={404: {"message": "Not found"}}
)


@router.get("/{run_id}/next")
def show_next_task(*, db: Session = Depends(get_db), run_id: UUID) -> Any:
    """
    Retrieve running instance and return next task(s).
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # TODO

    return run


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

    # TODO

    return run


@router.put("/{run_id}/step/{step_id}")
def exec_specific_task_actions(
    *, db: Session = Depends(get_db), run_id: UUID, step_id: UUID, actions: dict
) -> Any:
    """
    Perform actions for a given execution step.
    """
    run = RunController.get(db=db, id=run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # TODO

    return run


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

    # TODO

    return run
