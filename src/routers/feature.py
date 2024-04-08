from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.FeatureController import FeatureController
from src.dependencies.authentication import validate_user
from src.schemas.FeatureSchema import (
    Feature,
    FeatureCreate,
    FeatureUpdate,
)

router = APIRouter(
    prefix="/feature",
    tags=["Features"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("", response_model=dict[str, Any | list[Feature]])
def read_features(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve features with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return FeatureController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at": None}
    )


@router.post("")
def create_feature(*, db: Session = Depends(get_db), feature_in: FeatureCreate) -> Any:
    """
    Create new feature.
    """
    return FeatureController.create(db=db, obj_in=feature_in)


@router.get("/deleted", response_model=dict[str, Any | list[Feature]])
def read_deleted_features(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted features.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return FeatureController.read_multi(
        db, skip, limit, order, direction, criteria={"deleted_at__not": None}
    )


@router.get("/deleted/{feature_id}", response_model=Feature)
def read_deleted_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: UUID,
) -> Any:
    """
    Get deleted feature by ID.
    """
    return FeatureController.read(
        db=db, resource_id=feature_id, criteria={"deleted_at__not": None}
    )


@router.get("/{feature_id}", response_model=Feature)
def read_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: UUID,
) -> Any:
    """
    Get feature by ID.
    """
    return FeatureController.read(
        db=db, resource_id=feature_id, criteria={"deleted_at": None}
    )


@router.put("/{feature_id}", response_model=Feature)
def update_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: UUID,
    feature_in: FeatureUpdate,
) -> Any:
    """
    Update a feature.
    """
    return FeatureController.update(
        db=db, resource_id=feature_id, resource_in=feature_in
    )


@router.delete("/{feature_id}", response_model=Feature)
def destroy_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: UUID,
) -> Any:
    """
    Delete a feature.
    """
    return FeatureController.destroy(
        db=db, resource_id=feature_id, resource_in=FeatureUpdate()
    )


@router.delete("/{feature_id}/revert", response_model=Feature)
def revert_feature(
    *,
    db: Session = Depends(get_db),
    feature_id: UUID,
) -> Any:
    """
    Revert the deletion of a feature.
    """
    return FeatureController.revert(
        db=db, resource_id=feature_id, resource_in=FeatureUpdate()
    )
