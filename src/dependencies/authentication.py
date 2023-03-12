from datetime import datetime, timedelta, timezone
from fastapi import Depends, Header
from fastapi.encoders import jsonable_encoder
from json import loads
from sqlalchemy.orm import Session
from src.clients.crypto import client
from src.controllers.OAuthController import OAuthController
from src.controllers.UserController import UserController
from src.database import get_db
from src.errors.ApiRequestException import BadRequestException, UnauthorizedException
from src.schemas.UserSchema import UserUpdate


def _prepare_token(x_es_token, db, raise_a_raise=True):
    if x_es_token == None or x_es_token == "null":
        return (None, None, None)

    try:
        decrypted = loads(client.decrypt(x_es_token))
    except:
        raise BadRequestException(message="X-ES-Token header is invalid")

    user_id = decrypted["user"]
    token_id = decrypted["token"]

    try:
        user = UserController.read(db, user_id, {"is_active": True})
    except:
        if raise_a_raise:
            raise UnauthorizedException(message="User does not exist, or is inactive")

    if token_id not in user.session.keys():
        if raise_a_raise:
            raise UnauthorizedException(message="Token does not exist")

    token = user.session.get(token_id)

    return (user, token, token_id)


def _remove_session(db, user, token_id, error_message="", raise_a_raise=True):
    parsed_sessions = jsonable_encoder(user.session)
    try:
        del parsed_sessions[token_id]
    except:
        if raise_a_raise:
            raise UnauthorizedException(message="Token does not exist for this User")

    UserController.update(
        db,
        resource_id=user.id,
        resource_in=UserUpdate(session=parsed_sessions),
    )

    if raise_a_raise:
        raise UnauthorizedException(message=error_message)


def _parse_mode(date_now, token):
    access_token_expire_datetime = datetime.fromisoformat(token["expires_in"])
    refresh_token_expire_datetime = datetime.fromisoformat(token["refresh_expires_in"])

    if date_now < access_token_expire_datetime:
        return "access_valid"
    elif date_now < refresh_token_expire_datetime:
        return "refresh_valid"
    else:
        return "expired"


async def validate_user(x_es_token: str = Header(), db: Session = Depends(get_db)):
    user, token, token_id = _prepare_token(x_es_token, db)

    if not token:
        raise UnauthorizedException(message="Invalid Access Token")

    date_now = datetime.now(tz=timezone.utc)

    mode = _parse_mode(date_now, token)

    if mode == "access_valid":
        try:
            OAuthController.get_user_info(token)
        except:
            _remove_session(
                db, user, token_id, "Invalid Access Token! Please sign in again"
            )
    elif mode == "refresh_valid":
        try:
            token = OAuthController.refresh_token(token)

            parsed_token = token
            parsed_token["expires_in"] = (
                date_now + timedelta(seconds=token["expires_in"])
            ).isoformat()
            parsed_token["refresh_expires_in"] = (
                date_now + timedelta(seconds=token["refresh_expires_in"])
            ).isoformat()

            parsed_sessions = jsonable_encoder(user.session)
            parsed_sessions[token_id] = parsed_token

            UserController.update(
                db,
                resource_id=user.id,
                resource_in=UserUpdate(session=parsed_sessions),
            )
        except:
            _remove_session(
                db, user, token_id, "Invalid Refresh Token! Please sign in again"
            )
    else:
        raise UnauthorizedException(message="Invalid Access Token")

    return (user, token, token_id)


async def clean_before_login(
    x_es_token: str = Header(default=""), db: Session = Depends(get_db)
):
    if x_es_token:
        user, _, token_id = _prepare_token(x_es_token, db, False)

        if user and token_id:
            _remove_session(db, user, token_id, raise_a_raise=False)
