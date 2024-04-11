from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError


class BaseRouter:
    def __init__(self, host: str) -> None:
        self.host = host


class BaseApi:
    def __init__(self, Router: BaseRouter, host: str) -> None:
        self.router = Router(host)
        self.session = Session()

        self.session.mount(host, HTTPAdapter(max_retries=3))

    def _response_wrapper(self, response: Response) -> dict:
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as err:
                return {
                    "error": err.response.json(),
                    "is_success": False,
                    "code": response.status_code,
                }

        custom_response = response.json()
        custom_response["is_success"] = True

        return custom_response
