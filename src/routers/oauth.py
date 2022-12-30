from typing import Any
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from src.controllers.OAuthController import OAuthController
from src.config import OAUTH_HOST, OAUTH_TOKEN_URL
from src.dependencies.authentication import clean_before_login

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
