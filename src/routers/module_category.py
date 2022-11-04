from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.controllers.ModuleCategoryController import ModuleCategoryController
from src.schemas.ModuleCategorySchema import (
    ModuleCategory,
    ModuleCategoryCreate,
    ModuleCategoryUpdate,
)
from ._base import RouteHelper

route_helper = RouteHelper(ModuleCategoryController)

router = APIRouter(
    prefix="/category/module",
    tags=["Module Categories"],
    responses={404: {"message": "Not found"}},
)


@router.get("", response_model=dict[str, Any | list[ModuleCategory]])
def read_module_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve module categories with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return route_helper.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


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


@router.get("/deleted", response_model=dict[str, Any | list[ModuleCategory]])
def read_deleted_module_categories(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted module categories.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return route_helper.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at__not": None}
    )


@router.get("/deleted/{category_id}", response_model=ModuleCategory)
def read_deleted_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get deleted category by ID.
    """
    return route_helper.read(category_id, db=db, criteria={"deleted_at__not": None})


@router.get("/{category_id}", response_model=ModuleCategory)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get category by ID.
    """
    return route_helper.read(category_id, db=db, criteria={"deleted_at": None})


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
    category = route_helper.read(category_id, db=db, criteria={"deleted_at": None})

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
    category = route_helper.read(category_id, db=db, criteria={"deleted_at": None})

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
    category = route_helper.read(category_id, db=db, criteria={"deleted_at__not": None})

    if not category.deleted_at:
        raise HTTPException(status_code=405, detail="Module Category is active")

    category_in = ModuleCategoryUpdate(code=category.code, name=category.name)
    category_in.deleted_at = None
    category = ModuleCategoryController.update(
        db=db, db_obj=category, obj_in=category_in
    )
    return category
