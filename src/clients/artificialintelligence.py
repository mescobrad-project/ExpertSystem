from .classes.BaseApi import BaseApi, BaseRouter
from src.config import AI_API_BASE_URL
from uuid import UUID


class Router(BaseRouter):
    def healthcheck(self) -> str:
        """
        :return: {host}/healthcheck
        """
        return f"{self.host}/healthcheck"

    def algo(self) -> str:
        """
        :return: {host}/algo
        """
        return f"{self.host}/algo"

    def regression(self) -> str:
        """
        :return: {host}/algo/regression
        """
        return f"{self.algo()}/regression"

    def regression_svn(self) -> str:
        """
        :return: {host}/algo/regression/svn
        """
        return f"{self.regression()}/svn"

    def regression_svn_train(self) -> str:
        """
        :return: {host}/algo/regression/svn/train
        """
        return f"{self.regression_svn()}/train"

    def check_if_route_is_available(self, route_name) -> bool:
        """
        :return: if route is available in specific list
        """
        return f"{self.algo()}/{route_name}" in [
            self.regression_svn(),
        ]


class Api(BaseApi):
    def get_healthcheck(self) -> dict:
        return self._response_wrapper(self.session.get(self.router.healthcheck()))

    def post_regression_svn_train(self, data: dict) -> dict:
        return self._response_wrapper(
            self.session.post(self.router.regression_svn_train(), json=data)
        )


client = Api(Router, AI_API_BASE_URL)
