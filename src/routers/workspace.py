from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.PlatformUserDefaultWorkspaceController import (
    PlatformUserDefaultWorkspaceController,
)
from src.dependencies.authentication import validate_user, get_user_only
from src.schemas.PlatformWorkspaceSchema import PlatformWorkspace

router = APIRouter(
    prefix="/workspace",
    tags=["Workspaces"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("/user", response_model=list[PlatformWorkspace])
def read_users_workspaces(
    db: Session = Depends(get_db), user: int = Depends(get_user_only)
) -> Any:
    """
    Retrieve workspaces that logged in user has access.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    return PlatformUserDefaultWorkspaceController.read_multi(
        db,
        criteria={"user_name": user.info["preferred_username"]},
    )
