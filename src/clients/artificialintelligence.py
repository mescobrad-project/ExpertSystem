from requests import Session
from requests.adapters import HTTPAdapter
from src.config import AI_API_BASE_URL
from uuid import UUID


class Route:
    def __init__(self, host: str) -> None:
        self.host = host

    def algo(self) -> str:
        return f"{self.host}/algo"


class Api:
    def __init__(self, host: str) -> None:
        self.route = Route(host)
        self.session = Session()

        self.session.mount(host, HTTPAdapter(max_retries=3))

    def post_algo(self, data: dict) -> dict:
        response = self.session.post(self.route.algo(), json=data)

        if not response.ok:
            return {}

        return response.json()


client = Api(AI_API_BASE_URL)
