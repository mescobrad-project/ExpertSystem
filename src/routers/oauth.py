from typing import Any
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
from sqlalchemy.orm import Session
from src.clients.keycloak import BaseOAuthClient
from src.controllers.OAuthController import OAuthController
from src.config import (
    OAUTH_CLIENT_ID,
    OAUTH_CLIENT_SECRET,
    OAUTH_HOST,
    OAUTH_REALM,
    OAUTH_TOKEN_URL,
    ES_UI_BASE_URL,
)
from src.database import get_db
from src.dependencies.authentication import clean_before_login, validate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"message": "Not found"}},
)

keycloack = KeycloakOpenID(
    server_url=OAUTH_HOST,
    client_id=OAUTH_CLIENT_ID,
    realm_name=OAUTH_REALM,
    client_secret_key=OAUTH_CLIENT_SECRET,
    verify=True,
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


@router.get("/callback")
def oauth_callback(
    *,
    db: Session = Depends(get_db),
    code: str,
    clean_token=Depends(clean_before_login),
) -> Any:
    """
    Route used to retrieve auth token.
    """
    token, user, actual_token, refresh_token = OAuthController.oauth_callback(db, code)
    return RedirectResponse(
        url=f"{ES_UI_BASE_URL}/auth/callback/{user}/{token}/{actual_token}/{refresh_token}"
    )


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


@router.get("/refresh")
def refresh_token(*, db: Session = Depends(get_db), request: Request) -> Any:
    """
    Refresh token
    """
    new_token = keycloack.refresh_token(request.headers.get("x-refresh-token"))
    return {"status": 200, "success": True, "token": new_token}
