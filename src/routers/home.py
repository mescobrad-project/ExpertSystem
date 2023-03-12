from typing import Any
from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.config import ES_UI_BASE_URL
from src.database import get_db
from src.controllers.OAuthController import OAuthController
from src.dependencies.authentication import clean_before_login

router = APIRouter(prefix="", tags=["home"], responses={404: {"message": "Not found"}})


@router.get("/healthcheck")
def get_app_healthcheck() -> Any:
    """
    Route used to check if app is up and ready.
    """

    return {"status": 200, "success": True}


@router.get("/")
def oauth_callback(
    *,
    db: Session = Depends(get_db),
    code: str,
    clean_token=Depends(clean_before_login),
) -> Any:
    """
    Route used to retrieve auth token.
    """
    token, user = OAuthController.oauth_callback(db, code)
    return Response(
        f"<html><body><script defer>window.location.assign('{ES_UI_BASE_URL}/auth/callback/{user}/{token}')</script></body></html>"
    )
