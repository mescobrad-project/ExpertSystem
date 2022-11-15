from .classes.BaseApi import BaseApi, BaseRouter
from src.config import DA_API_BASE_URL
from src.schemas.ExternalApiSchema import DataAnalyticsInput


class Router(BaseRouter):
    def navigation(self) -> str:
        """
        :return: {host}/function/navigation/
        """
        return f"{self.host}/function/navigation/"

    def existing(self) -> str:
        """
        :return: {host}/function/existing
        """
        return f"{self.host}/function/existing"


class Api(BaseApi):
    def post(self, data: DataAnalyticsInput) -> dict:
        return self._response_wrapper(
            self.session.post(self.router.navigation(), json=data)
        )

    def check_if_function_exists(self, func_name: str) -> bool:
        response = self._response_wrapper(self.session.get(self.router.existing()))

        if not response["is_success"]:
            return False

        return func_name in response["analytics-functions"]


client = Api(Router, DA_API_BASE_URL)
