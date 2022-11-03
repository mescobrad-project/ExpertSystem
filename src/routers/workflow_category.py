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

router = APIRouter(
    prefix="/category/workflow",
    tags=["Workflow Category"],
    responses={404: {"message": "Not found"}},
)


@router.get("", response_model=list[WorkflowCategory])
def read_workflow_categories(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve workflow categories with their metadata.
    """
    try:
        categories = WorkflowCategoryController.get_multi(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return categories


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


@router.get("/deleted", response_model=list[WorkflowCategory])
def read_deleted_workflow_categories(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve deleted workflow categories.
    """
    try:
        categories = WorkflowCategoryController.get_multi_deleted(
            db, skip=skip, limit=limit
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return categories


@router.get("/deleted/{category_id}", response_model=WorkflowCategory)
def read_deleted_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get deleted workflow category by ID.
    """
    category = WorkflowCategoryController.get_deleted(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Workflow Category not found")

    return category


@router.get("/{category_id}", response_model=WorkflowCategory)
def read_workflow_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get workflow category by ID.
    """
    category = WorkflowCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Workflow Category not found")

    return category


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
    category = WorkflowCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Workflow Category not found")

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
    category = WorkflowCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Workflow Category not found")

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
    category = WorkflowCategoryController.get_deleted(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Workflow Category not found")

    if not category.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow Category is active")

    category_in = WorkflowCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = None
    category = WorkflowCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category
