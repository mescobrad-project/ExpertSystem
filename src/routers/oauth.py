from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from src.controllers.OAuthController import OAuthController
from src.config import OAUTH_HOST, OAUTH_TOKEN_URL
from src.database import get_db
from src.dependencies.authentication import clean_before_login, validate_user

router = APIRouter(
    prefix="/oauth",
    tags=["Authentication"],
    responses={404: {"message": "Not found"}},
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=OAUTH_HOST, tokenUrl=OAUTH_TOKEN_URL
)


@router.get("/login", dependencies=[Depends(clean_before_login)])
def get_auth() -> Any:
    """
    Get OAuth endpoint to redirect to log in.
    """
    return {"url": OAuthController.login()}


@router.get("/logout")
def oauth_logout(
    *,
    db: Session = Depends(get_db),
    auth_validation=Depends(validate_user),
) -> Any:
    """
    Logout used.
    """
    (user, token, token_id) = auth_validation
    OAuthController.logout(db, user, token, token_id)

    return {"status": 200, "success": True}
