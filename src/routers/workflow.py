from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.controllers.WorkflowController import WorkflowController
from src.schemas.WorkflowSchema import Workflow, WorkflowCreate, WorkflowUpdate
from src.controllers.RunController import RunController
from src.schemas.RunSchema import Run, RunUpdate
from src.controllers.WorkflowEngineController import WorkflowEngineController

router = APIRouter(
    prefix="/workflow", tags=["workflow"], responses={404: {"message": "Not found"}}
)


@router.get("/", response_model=list[Workflow])
def read_workflows(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve workflows with their metadata.
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

        workflow_upd = WorkflowUpdate()
        workflow_upd.tasks = WorkflowController.parse_xml(
            workflow.raw_diagram_data["xml_original"]
        )
        workflow = WorkflowController.update(
            db=db, db_obj=workflow, obj_in=workflow_upd
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workflow already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return workflow


@router.get("/entity_types")
def read_entity_types() -> Any:
    """
    Get all available workflow entity types.
    """
    entity_types = WorkflowController.get_workflow_entity_types()
    if not entity_types:
        raise HTTPException(status_code=404, detail="Entities not found")

    return entity_types


@router.get("/deleted", response_model=list[Workflow])
def read_deleted_workflows(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve deleted workflows.
    """
    try:
        workflows = WorkflowController.get_multi_deleted(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return workflows


@router.get("/deleted/{workflow_id}", response_model=Workflow)
def read_deleted_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get deleted workflow by ID.
    """
    workflow = WorkflowController.get_deleted(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

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

    workflow_in.tasks = WorkflowController.parse_xml(
        workflow.raw_diagram_data["xml_original"]
    )
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


@router.get("/{workflow_id}/task/{task_name}")
def read_task_details(
    *, db: Session = Depends(get_db), workflow_id: UUID, task_name: str
) -> Any:
    """
    Get task details given its name and workflow ID.
    """
    workflow = WorkflowController.get(db=db, id=workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    for key, task in workflow.tasks.items():
        if key == task_name:
            return task

    raise HTTPException(status_code=404, detail="Task not found")
