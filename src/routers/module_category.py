from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
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
    return ModuleCategoryController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


@router.post("")
def create_category(
    *, db: Session = Depends(get_db), category_in: ModuleCategoryCreate
) -> Any:
    """
    Create new category.
    """
    return ModuleCategoryController.create(db=db, obj_in=category_in)


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
    return ModuleCategoryController.read_multi(
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
    return ModuleCategoryController.read(
        db=db, resource_id=category_id, criteria={"deleted_at__not": None}
    )


@router.get("/{category_id}", response_model=ModuleCategory)
def read_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Get category by ID.
    """
    return ModuleCategoryController.read(
        db=db, resource_id=category_id, criteria={"deleted_at": None}
    )


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
    return ModuleCategoryController.update(
        db=db, resource_id=category_id, resource_in=category_in
    )


@router.delete("/{category_id}", response_model=ModuleCategory)
def destroy_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Delete a category.
    """
    return ModuleCategoryController.destroy(
        db=db, resource_id=category_id, resource_in=ModuleCategoryUpdate()
    )


@router.delete("/{category_id}/revert", response_model=ModuleCategory)
def revert_category(
    *,
    db: Session = Depends(get_db),
    category_id: UUID,
) -> Any:
    """
    Revert the deletion of a category.
    """
    return ModuleCategoryController.revert(
        db=db, resource_id=category_id, resource_in=ModuleCategoryUpdate()
    )
