from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.VariableController import VariableController
from src.dependencies.authentication import validate_user
from src.schemas.VariableSchema import (
    Variable,
    VariableCreate,
    VariableUpdate,
)

router = APIRouter(
    prefix="/variable",
    tags=["Variables"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("", response_model=dict[str, Any | list[Variable]])
def read_variables(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve variables with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return VariableController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


@router.post("")
def create_variable(
    *, db: Session = Depends(get_db), variable_in: VariableCreate
) -> Any:
    """
    Create new variable.
    """
    return VariableController.create(db=db, obj_in=variable_in)


@router.get("/deleted", response_model=dict[str, Any | list[Variable]])
def read_deleted_variables(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted variables.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return VariableController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at__not": None}
    )


@router.get("/deleted/{variable_id}", response_model=Variable)
def read_deleted_variable(
    *,
    db: Session = Depends(get_db),
    variable_id: UUID,
) -> Any:
    """
    Get deleted variable by ID.
    """
    return VariableController.read(
        db=db, resource_id=variable_id, criteria={"deleted_at__not": None}
    )


@router.get("/{variable_id}", response_model=Variable)
def read_variable(
    *,
    db: Session = Depends(get_db),
    variable_id: UUID,
) -> Any:
    """
    Get variable by ID.
    """
    return VariableController.read(
        db=db, resource_id=variable_id, criteria={"deleted_at": None}
    )


@router.put("/{variable_id}", response_model=Variable)
def update_variable(
    *,
    db: Session = Depends(get_db),
    variable_id: UUID,
    variable_in: VariableUpdate,
) -> Any:
    """
    Update a variable.
    """
    return VariableController.update(
        db=db, resource_id=variable_id, resource_in=variable_in
    )


@router.delete("/{variable_id}", response_model=Variable)
def destroy_variable(
    *,
    db: Session = Depends(get_db),
    variable_id: UUID,
) -> Any:
    """
    Delete a variable.
    """
    return VariableController.destroy(
        db=db, resource_id=variable_id, resource_in=VariableUpdate()
    )


@router.delete("/{variable_id}/revert", response_model=Variable)
def revert_variable(
    *,
    db: Session = Depends(get_db),
    variable_id: UUID,
) -> Any:
    """
    Revert the deletion of a variable.
    """
    return VariableController.revert(
        db=db, resource_id=variable_id, resource_in=VariableUpdate()
    )
