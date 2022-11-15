from .classes.BaseApi import BaseApi, BaseRouter
from src.config import QB_API_BASE_URL


class Router(BaseRouter):
    pass


class Api(BaseApi):
    def redirect(self) -> str:
        return self.router.host


client = Api(Router, QB_API_BASE_URL)
