from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.controllers.WorkflowCategoryController import WorkflowCategoryController
from src.schemas.WorkflowCategorySchema import (
    WorkflowCategory,
    WorkflowCategoryCreate,
    WorkflowCategoryUpdate,
)
from ._base import RouteHelper

route_helper = RouteHelper(WorkflowCategoryController)

router = APIRouter(
    prefix="/category/workflow",
    tags=["Workflow Category"],
    responses={404: {"message": "Not found"}},
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
    return route_helper.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


@router.post("")
def create_workflow_category(
    *, db: Session = Depends(get_db), category_in: WorkflowCategoryCreate
) -> Any:
    """
    Create new workflow category.
    """
    try:
        category = WorkflowCategoryController.create(db=db, obj_in=category_in)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workflow Category already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return category


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
    return route_helper.read_multi(
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
    return route_helper.read(category_id, db=db, criteria={"deleted_at__not": None})


@router.get("/{category_id}", response_model=WorkflowCategory)
def read_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get workflow category by ID.
    """
    return route_helper.read(category_id, db=db, criteria={"deleted_at": None})


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
    category = route_helper.read(category_id, db=db, criteria={"deleted_at": None})

    category = WorkflowCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category


@router.delete("/{category_id}", response_model=WorkflowCategory)
def destroy_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Delete a workflow category.
    """
    category = route_helper.read(category_id, db=db, criteria={"deleted_at": None})

    if category.deleted_at:
        raise HTTPException(
            status_code=405, detail="Workflow Category already destroyed"
        )

    category_in = WorkflowCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = datetime.now(tz=timezone.utc)
    category = WorkflowCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category


@router.delete("/{category_id}/revert", response_model=WorkflowCategory)
def revert_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow category.
    """
    category = route_helper.read(category_id, db=db, criteria={"deleted_at__not": None})

    if not category.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow Category is active")

    category_in = WorkflowCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = None
    category = WorkflowCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category
