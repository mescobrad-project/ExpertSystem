from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.controllers.WorkflowController import WorkflowController
from src.schemas.WorkflowSchema import Workflow, WorkflowCreate, WorkflowUpdate

router = APIRouter(
    prefix="/workflow", tags=["workflow"], responses={404: {"message": "Not found"}}
)


@router.get("/", response_model=list[Workflow])
def read_workflows(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve worflows with their metadata.
    """
    try:
        workflows = WorkflowController.get_multi(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return workflows


@router.post("/")
def create_workflow(
    *, db: Session = Depends(get_db), workflow_in: WorkflowCreate
) -> Any:
    """
    Create new workflow.
    """
    try:
        workflow = WorkflowController.create(db=db, obj_in=workflow_in)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workflow already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return workflow


@router.get("/{workflow_id}", response_model=Workflow)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get workflow by ID.
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return workflow


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
    workflow_in: WorkflowUpdate,
) -> Any:
    """
    Update a workflow.
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.delete("/{workflow_id}", response_model=Workflow)
def destroy_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Delete a workflow.
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if workflow.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow already destroyed")

    workflow_in = WorkflowUpdate()
    workflow_in.deleted_at = datetime.now(tz=timezone.utc)
    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.delete("/{workflow_id}/revert", response_model=Workflow)
def revert_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow.
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not workflow.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow is active")

    workflow_in = WorkflowUpdate()
    workflow_in.deleted_at = None
    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


# @router.get("/{workflow_id}/run", response_model=WorkflowBase.Run)
# def run_workflow(workflow_id: str, db: Session = Depends(get_db)):
#     db_run = createRun(db, workflow_id=workflow_id)

#     # db_workflow = read_one(db, workflow_id=workflow_id)
#     # db_run.next_steps = engine.Init(db_workflow.file, db_run.id)
#     db_run.next_steps = engine.Init("simple.json", db_run.id)
#     engine.CompleteStep(workflow_id, f"{db_run.id}.json")
#     return db_run


# @router.get("/{workflow_id}/task/{task_name}")
# def run_workflow(workflow_id: str, task_name: str, db: Session = Depends(get_db)):
#     # db_workflow = read_one(db, workflow_id=workflow_id)
#     # task = engine.GetTaskDetails(db_workflow.file, task_name)
#     try:
#         task = engine.GetTaskDetails("simple.json", task_name)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     return task
