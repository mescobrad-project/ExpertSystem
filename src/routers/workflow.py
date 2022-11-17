from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.WorkflowModel import WorkflowModel
from src.controllers.WorkflowController import WorkflowController
from src.schemas.WorkflowSchema import Workflow, WorkflowCreate, WorkflowUpdate
from src.controllers.RunController import RunController
from src.schemas.RunSchema import Run

router = APIRouter(
    prefix="/workflow", tags=["workflow"], responses={404: {"message": "Not found"}}
)


@router.get("", response_model=dict[str, Any | list[Workflow]])
def read_workflows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    is_template: bool = False,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve workflows with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return WorkflowController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        is_template,
        category,
        criteria={"deleted_at": None},
    )


@router.post("")
def create_workflow(
    *, db: Session = Depends(get_db), workflow_in: WorkflowCreate
) -> Any:
    """
    Create new workflow.
    """
    return WorkflowController.create(db=db, obj_in=workflow_in)


@router.get("/entity_types")
def read_entity_types() -> Any:
    """
    Get all available workflow entity types.
    """
    return WorkflowController.read_entity_types()


@router.get("/deleted", response_model=dict[str, Any | list[Workflow]])
def read_deleted_workflows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    is_template: bool = False,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted workflows.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return WorkflowController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        is_template,
        category,
        criteria={"deleted_at__not": None},
    )


@router.get("/deleted/{workflow_id}", response_model=Workflow)
def read_deleted_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get deleted workflow by ID.
    """
    return WorkflowController.read(
        db=db, resource_id=workflow_id, criteria={"deleted_at__not": None}
    )


@router.get("/{workflow_id}", response_model=Workflow)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get workflow by ID.
    """
    return WorkflowController.read(
        db=db, resource_id=workflow_id, criteria={"deleted_at": None}
    )


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
    return WorkflowController.update(
        db=db, resource_id=workflow_id, resource_in=workflow_in
    )


@router.delete("/{workflow_id}", response_model=Workflow)
def destroy_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Delete a workflow.
    """
    return WorkflowController.destroy(
        db=db, resource_id=workflow_id, resource_in=WorkflowUpdate()
    )


@router.delete("/{workflow_id}/revert", response_model=Workflow)
def revert_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow.
    """
    return WorkflowController.revert(
        db=db, resource_id=workflow_id, resource_in=WorkflowUpdate()
    )


@router.get("/{workflow_id}/task/{task_name}")
def read_task_details(
    *, db: Session = Depends(get_db), workflow_id: UUID, task_name: str
) -> Any:
    """
    Get task details given its name and workflow ID.
    """
    return WorkflowController.read_task_details(
        db=db, resource_id=workflow_id, task_name=task_name
    )


@router.get("/{workflow_id}/run", response_model=dict[str, Any | list[Run]])
def read_workflow_runs(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve running instances of specific workflow.
    """
    return RunController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        {
            "workflow_id": workflow_id,
            "workflow": {"model": WorkflowModel, "criteria": {"deleted_at": None}},
        },
    )
