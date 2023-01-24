from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from urllib.parse import unquote_plus
from src.database import get_db
from src.controllers.FileController import FileController
from src.dependencies.authentication import validate_user

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
    return FileController.search(db, term=unquote_plus(term))
