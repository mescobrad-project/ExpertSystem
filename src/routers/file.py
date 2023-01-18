from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.FileController import FileController
from src.dependencies.authentication import validate_user
from src.schemas.FileSchema import (
    FileSearch,
    FileCreate,
    FileUpdate,
)

router = APIRouter(
    prefix="/file",
    tags=["Files"],
    responses={404: {"message": "Not found"}},
    dependencies=[Depends(validate_user)],
)


@router.get("")
def read_files(
    db: Session = Depends(get_db),
    term: str = "",
) -> Any:
    """
    Retrieve files with their metadata.
    """
    return FileController.search(db, term=term)
