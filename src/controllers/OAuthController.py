from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from json import dumps
from sqlalchemy.orm import Session
from uuid import uuid4
from src.clients.crypto import client as crypto
from src.clients.keycloak import client, BaseOAuthClient
from src.errors.ApiRequestException import NotFoundException
from src.schemas.UserSchema import UserCreate, UserUpdate
from .UserController import UserController


class BaseController:
    __client: BaseOAuthClient

    def __init__(self, client):
        self.__client = client

    def login(self):
        return self.__client.get_auth_code()

    def token(self, code: str):
        return self.__client.get_access_token(code)

    def get_user_info(self, token=Depends(token)):
        return self.__client.get_user_info(token["access_token"])

    def refresh_token(self, token=Depends(token)):
        return self.__client.refresh_token(token["refresh_token"])

    def oauth_callback(self, db: Session, code: str):
        token = self.token(code)
        user_info = self.get_user_info(token)

        date_now = datetime.now(tz=timezone.utc)

        token_id = str(uuid4())
        parsed_token = token
        parsed_token["expires_in"] = (
            date_now + timedelta(seconds=token["expires_in"])
        ).isoformat()
        parsed_token["refresh_expires_in"] = (
            date_now + timedelta(seconds=token["refresh_expires_in"])
        ).isoformat()

        try:
            user_db = UserController.get_from_sub_and_provider(
                db, sub=user_info["sub"], provider="keycloak"
            )

            parsed_sessions = jsonable_encoder(user_db.session)
            parsed_sessions[token_id] = parsed_token

            user_db = UserController.update(
                db,
                resource_id=user_db.id,
                resource_in=UserUpdate(
                    info={
                        "name": user_info["name"],
                        "preferred_username": user_info["preferred_username"],
                        "given_name": user_info["given_name"],
                        "family_name": user_info["family_name"],
                        "email": user_info["email"],
                    },
                    permission=user_info["resource_access"],
                    session=parsed_sessions,
                ),
            )
        except NotFoundException:
            user_db = UserController.create(
                db,
                obj_in=UserCreate(
                    sub=user_info["sub"],
                    provider="keycloak",
                    is_active=True,
                    info={
                        "name": user_info["name"],
                        "preferred_username": user_info["preferred_username"],
                        "given_name": user_info["given_name"],
                        "family_name": user_info["family_name"],
                        "email": user_info["email"],
                    },
                    permission=user_info["resource_access"],
                    session={token_id: parsed_token},
                ),
            )

        return {
            "token": crypto.encrypt(
                dumps({"user": str(user_db.id), "token": token_id}).encode("utf-8")
            )
        }


OAuthController = BaseController(client)
