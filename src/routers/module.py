from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.ModuleController import ModuleController
from src.schemas.ModuleSchema import (
    Module,
    ModuleCreate,
    ModuleUpdate,
)

router = APIRouter(
    prefix="/module",
    tags=["Modules"],
    responses={404: {"message": "Not found"}},
)


@router.get("", response_model=dict[str, Any | list[Module]])
def read_modules(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    task: str = None,
    category: str = None,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve module with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return ModuleController.read_multi(
        db, skip, limit, order, direction, task, category, criteria={"deleted_at": None}
    )


@router.post("")
def create_module(*, db: Session = Depends(get_db), module_in: ModuleCreate) -> Any:
    """
    Create new module.
    """
    return ModuleController.create(db=db, obj_in=module_in)


@router.get("/deleted", response_model=dict[str, Any | list[Module]])
def read_modules(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    task: str = None,
    category: str = None,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted module.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return ModuleController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        task,
        category,
        criteria={"deleted_at__not": None},
    )


@router.get("/deleted/{module_id}", response_model=Module)
def read_deleted_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Get deleted module by ID.
    """
    return ModuleController.read(
        db=db, resource_id=module_id, criteria={"deleted_at__not": None}
    )


@router.get("/{module_id}", response_model=Module)
def read_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Get module by ID.
    """
    return ModuleController.read(
        db=db, resource_id=module_id, criteria={"deleted_at": None}
    )


@router.put("/{module_id}", response_model=Module)
def update_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
    module_in: ModuleUpdate,
) -> Any:
    """
    Update a module.
    """
    return ModuleController.update(db=db, resource_id=module_id, resource_in=module_in)


@router.delete("/{module_id}", response_model=Module)
def destroy_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Delete a module.
    """
    return ModuleController.destroy(
        db=db, resource_id=module_id, resource_in=ModuleUpdate()
    )


@router.delete("/{module_id}/revert", response_model=Module)
def revert_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Revert the deletion of a module.
    """
    return ModuleController.revert(
        db=db, resource_id=module_id, resource_in=ModuleUpdate()
    )
