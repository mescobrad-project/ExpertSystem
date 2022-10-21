from requests import Response, Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError


class BaseRouter:
    def __init__(self, host: str) -> None:
        self.host = host


class BaseApi:
    def __init__(self, Router: BaseRouter, host: str) -> None:
        self.route = Router(host)
        self.session = Session()

        self.session.mount(host, HTTPAdapter(max_retries=3))

    def _response_wrapper(self, response: Response) -> dict:
        if not response.ok:
            try:
                response.raise_for_status()
            except HTTPError as err:
                return {"error": err.response.json()}

        return response.json()
