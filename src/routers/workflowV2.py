from typing import Annotated, Any
from uuid import UUID
from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.models._all import WorkflowModel
from src.controllers.WorkflowController import WorkflowController
from src.schemas.NewWorkflowSchema import WorkflowBase
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user, get_user_only
from src.dependencies.workspace import validate_workspace
from src.schemas.RunSchema import Run
import uuid
from src.services.NewWorkflowsService import createWorkflow, getWorkflows

from src.models._all import (
    NewWorkflowModel,
    NewWorkflowStepModel,
    NewWorkflowActionModel,
    NewWorkflowActionConditionalModel,
)

router = APIRouter(
    prefix="/v2/workflow",
    tags=["workflow"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("/", response_model=dict[str, Any | list[WorkflowBase]])
def read_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
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
    return getWorkflows(db, ws_id, skip, limit, category, is_template, order, direction)


@router.post("/")
async def create_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
    workflow_in: WorkflowBase,
) -> Any:
    """
    Create new workflow.
    """
    return createWorkflow(db, workflow_in, ws_id)


@router.get("/deleted", response_model=dict[str, Any | list[WorkflowBase]])
def read_deleted_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
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
        criteria={"deleted_at__not": None, "ws_id": ws_id},
    )


@router.get("/deleted/{workflow_id}", response_model=WorkflowBase)
def read_deleted_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
    workflow_id: UUID,
) -> Any:
    """
    Get deleted workflow by ID.
    """
    return WorkflowController.read(
        db=db,
        resource_id=workflow_id,
        criteria={"deleted_at__not": None, "ws_id": ws_id},
    )


@router.get("/search", response_model=WorkflowBase)
def search_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
    name: str = None,
) -> Any:
    """
    Retrieve a workflow using search params.
    """
    return WorkflowController.search(
        db,
        params={"name": name},
        criteria={"deleted_at": None, "is_template": False, "ws_id": ws_id},
    )


@router.get("/{workflow_id}", response_model=WorkflowBase)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
    workflow_id: UUID,
) -> Any:
    """
    Get workflow by ID.
    """
    return WorkflowController.read(
        db=db, resource_id=workflow_id, criteria={"deleted_at": None, "ws_id": ws_id}
    )


@router.delete("/{workflow_id}", response_model=WorkflowBase)
def destroy_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Delete a workflow.
    """
    return WorkflowController.destroy(
        db=db, resource_id=workflow_id, resource_in=WorkflowBase()
    )


@router.delete("/{workflow_id}/revert", response_model=WorkflowBase)
def revert_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow.
    """
    return WorkflowController.revert(
        db=db, resource_id=workflow_id, resource_in=WorkflowBase()
    )


@router.get("/{workflow_id}/task/{task_sid}")
def read_task_details(
    *, db: Session = Depends(get_db), workflow_id: UUID, task_sid: str
) -> Any:
    """
    Get task details given its SID (e.g. Activity_04n854t) and workflow ID.
    """
    return WorkflowController.read_task_details(
        db=db, resource_id=workflow_id, task_sid=task_sid
    )


@router.get("/{workflow_id}/run", response_model=dict[str, Any | list[Run]])
def read_workflow_runs(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
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
            "workflow": {
                "model": WorkflowModel,
                "criteria": {"deleted_at": None, "ws_id": ws_id},
            },
            "ws_id": ws_id,
        },
    )
