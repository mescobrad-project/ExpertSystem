from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.models.ModuleModel import ModuleModel
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


@router.get("", response_model=list[Module])
def read_module(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve module with their metadata.
    """
    try:
        module = ModuleController.get_multi(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return module


@router.post("")
def create_module(*, db: Session = Depends(get_db), module_in: ModuleCreate) -> Any:
    """
    Create new module.
    """
    try:
        module = ModuleController.create(db=db, obj_in=module_in)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Module already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return module


@router.get("/deleted", response_model=list[Module])
def read_deleted_module(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve deleted module.
    """
    try:
        module = ModuleController.get_multi_deleted(db, skip=skip, limit=limit)
    except Exception:
        raise HTTPException(status_code=500, detail="Something went wrong")

    return module


@router.get("/deleted/{module_id}", response_model=Module)
def read_deleted_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Get deleted module by ID.
    """
    module = ModuleController.get_deleted(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    return module


@router.get("/{module_id}", response_model=Module)
def read_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Get module by ID.
    """
    module = ModuleController.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    return module


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
    module = ModuleController.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    module = ModuleController.update(db=db, db_obj=module, obj_in=module_in)
    return module


@router.delete("/{module_id}", response_model=Module)
def destroy_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Delete a module.
    """
    module = ModuleController.get(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if module.deleted_at:
        raise HTTPException(status_code=405, detail="Module already destroyed")

    module_in = ModuleUpdate(
        name=module.name, instructions=module.instructions, task=module.task
    )
    module_in.deleted_at = datetime.now(tz=timezone.utc)
    module = ModuleController.update(db=db, db_obj=module, obj_in=module_in)
    return module


@router.delete("/{module_id}/revert", response_model=Module)
def revert_module(
    *,
    db: Session = Depends(get_db),
    module_id: UUID,
) -> Any:
    """
    Revert the deletion of a module.
    """
    module = ModuleController.get_deleted(db=db, id=module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if not module.deleted_at:
        raise HTTPException(status_code=405, detail="Module is active")

    module_in = ModuleUpdate(
        name=module.name, instructions=module.instructions, task=module.task
    )
    module_in.deleted_at = None
    module = ModuleController.update(db=db, db_obj=module, obj_in=module_in)
    return module
