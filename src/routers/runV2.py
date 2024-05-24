from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user
from src.dependencies.workspace import validate_workspace
from src.schemas.RequestBodySchema import (
    TaskMetadataBodyParameter,
    CallActivityParams,
)
from src.schemas.RunSchema import Run, RunNameUpdate

router = APIRouter(
    prefix="/v2/run",
    tags=["run"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.post("/workflow/{workflow_id}", response_model=Run)
def run_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1,  # Depends(validate_workspace),
    workflow_id: UUID,
    data: dict = {},
):
    """
    Initiate a workflow process
    """
    return RunController.initialize(
        db=db,
        ws_id=ws_id,
        workflow_id=workflow_id,
        name=data.get("name", ""),
        settings=data.get("settings", {}),
    )

