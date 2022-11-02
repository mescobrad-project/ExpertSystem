from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.models.ModuleCategoryModel import ModuleCategoryModel
from src.controllers.ModuleCategoryController import ModuleCategoryController
from src.schemas.ModuleCategorySchema import (
    ModuleCategory,
    ModuleCategoryCreate,
    ModuleCategoryUpdate,
)

router = APIRouter(
    prefix="/category/module",
    tags=["Module Categories"],
    responses={404: {"message": "Not found"}},
)


@router.get("", response_model=list[ModuleCategory])
def read_module_categories(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve module categories with their metadata.
    """
    try:
        module_categories = ModuleCategoryController.get_multi(
            db, skip=skip, limit=limit
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return module_categories


@router.post("")
def create_category(
    *, db: Session = Depends(get_db), category_in: ModuleCategoryCreate
) -> Any:
    """
    Create new category.
    """
    try:
        category = ModuleCategoryController.create(db=db, obj_in=category_in)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Module Category already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return category


@router.get("/deleted", response_model=list[ModuleCategory])
def read_deleted_module_categories(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve deleted module categories.
    """
    try:
        module_categories = ModuleCategoryController.get_multi_deleted(
            db, skip=skip, limit=limit
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return module_categories


@router.get("/deleted/{category_id}", response_model=ModuleCategory)
def read_deleted_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get deleted category by ID.
    """
    category = ModuleCategoryController.get_deleted(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Module Category not found")

    return category


@router.get("/{category_id}", response_model=ModuleCategory)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get category by ID.
    """
    category = ModuleCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Module Category not found")

    return category


@router.put("/{category_id}", response_model=ModuleCategory)
def update_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
    category_in: ModuleCategoryUpdate,
) -> Any:
    """
    Update a category.
    """
    category = ModuleCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Module Category not found")

    category = ModuleCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category


@router.delete("/{category_id}", response_model=ModuleCategory)
def destroy_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Delete a category.
    """
    category = ModuleCategoryController.get(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Module Category not found")

    if category.deleted_at:
        raise HTTPException(status_code=405, detail="Module Category already destroyed")

    category_in = ModuleCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = datetime.now(tz=timezone.utc)
    category = ModuleCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category


@router.delete("/{category_id}/revert", response_model=ModuleCategory)
def revert_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Revert the deletion of a category.
    """
    category = ModuleCategoryController.get_deleted(db=db, id=category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Module Category not found")

    if not category.deleted_at:
        raise HTTPException(status_code=405, detail="Module Category is active")

    category_in = ModuleCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = None
    category = ModuleCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category
