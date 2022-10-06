from typing import Any
from fastapi import APIRouter

router = APIRouter(prefix="", tags=["home"], responses={404: {"message": "Not found"}})


@router.get("/healthcheck")
def get_app_healthcheck() -> Any:
    """
    Route used to check if app is up and ready.
    """

    return {"status": 200, "success": True}
