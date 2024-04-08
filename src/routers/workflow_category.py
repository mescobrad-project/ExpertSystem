from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.WorkflowCategoryController import WorkflowCategoryController
from src.dependencies.authentication import validate_user
from src.schemas.WorkflowCategorySchema import (
    WorkflowCategory,
    WorkflowCategoryCreate,
    WorkflowCategoryUpdate,
)

router = APIRouter(
    prefix="/category/workflow",
    tags=["Workflow Category"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("", response_model=dict[str, Any | list[WorkflowCategory]])
def read_workflow_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve workflow categories with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return WorkflowCategoryController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


@router.post("")
def create_workflow_category(
    *, db: Session = Depends(get_db), category_in: WorkflowCategoryCreate
) -> Any:
    """
    Create new workflow category.
    """
    return WorkflowCategoryController.create(db=db, obj_in=category_in)


@router.get("/deleted", response_model=dict[str, Any | list[WorkflowCategory]])
def read_deleted_workflow_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted workflow categories.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return WorkflowCategoryController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at__not": None}
    )


@router.get("/deleted/{category_id}", response_model=WorkflowCategory)
def read_deleted_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get deleted workflow category by ID.
    """
    return WorkflowCategoryController.read(
        db=db, resource_id=category_id, criteria={"deleted_at__not": None}
    )


@router.get("/{category_id}", response_model=WorkflowCategory)
def read_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get workflow category by ID.
    """
    return WorkflowCategoryController.read(
        db=db, resource_id=category_id, criteria={"deleted_at": None}
    )


@router.put("/{category_id}", response_model=WorkflowCategory)
def update_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
    category_in: WorkflowCategoryUpdate,
) -> Any:
    """
    Update a workflow category.
    """
    return WorkflowCategoryController.update(
        db=db, resource_id=category_id, resource_in=category_in
    )


@router.delete("/{category_id}", response_model=WorkflowCategory)
def destroy_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Delete a workflow category.
    """
    return WorkflowCategoryController.destroy(
        db=db, resource_id=category_id, resource_in=WorkflowCategoryUpdate()
    )


@router.delete("/{category_id}/revert", response_model=WorkflowCategory)
def revert_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow category.
    """
    return WorkflowCategoryController.revert(
        db=db, resource_id=category_id, resource_in=WorkflowCategoryUpdate()
    )
