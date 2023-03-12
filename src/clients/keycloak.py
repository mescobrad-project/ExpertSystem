from keycloak import KeycloakOpenID
from src.config import (
    OAUTH_HOST,
    OAUTH_CLIENT_SECRET,
    OAUTH_CLIENT_ID,
    OAUTH_CALLBACK_URL,
    OAUTH_REALM,
    OAUTH_LOGIN_SCOPE,
)


class BaseOAuthClient:
    __client: KeycloakOpenID

    def __init__(self, client):
        self.__client = client

    def get_well_known(self):
        return self.__client.well_known()

    def get_auth_code(self):
        return self.__client.auth_url(
            redirect_uri=OAUTH_CALLBACK_URL,
            scope=OAUTH_LOGIN_SCOPE,
            # state="your_state_info",
        )

    def get_access_token(self, code: str):
        return self.__client.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=OAUTH_CALLBACK_URL,
        )

    def refresh_token(self, refresh_token: str):
        return self.__client.refresh_token(refresh_token=refresh_token)

    def get_user_info(self, access_token: str):
        return self.__client.userinfo(access_token)

    def logout(self, refresh_token: str):
        return self.__client.logout(refresh_token)


client = BaseOAuthClient(
    KeycloakOpenID(
        server_url=OAUTH_HOST,
        client_id=OAUTH_CLIENT_ID,
        realm_name=OAUTH_REALM,
        client_secret_key=OAUTH_CLIENT_SECRET,
        verify=True,
    )
)
