from .classes.BaseApi import BaseApi, BaseRouter
from src.config import AI_API_BASE_URL


class Router(BaseRouter):
    def healthcheck(self) -> str:
        """
        :return: {host}/healthcheck
        """
        return f"{self.host}/healthcheck"

    def base_save_path(self) -> str:
        """
        :return: {host}/datalake/objectstorage/basepath
        """
        return f"{self.host}/datalake/objectstorage/basepath"

    def ai(self) -> str:
        """
        :return: {host}/ai
        """
        return f"{self.host}/ai"

    def regression(self) -> str:
        """
        :return: {ai}/regression
        """
        return f"{self.ai()}/regression"

    def regression_svr_train(self) -> str:
        """
        :return: {ai}/regression/svr/train
        """
        return f"{self.regression()}/svr/train"

    def regression_predict(self) -> str:
        """
        :return: {ai}/regression/predict
        """
        return f"{self.regression()}/predict"

    def classification(self) -> str:
        """
        :return: {ai}/classification
        """
        return f"{self.ai()}/classification"

    def classification_svc_train(self) -> str:
        """
        :return: {ai}/classification/svc/train
        """
        return f"{self.classification()}/svc/train"

    def classification_lda_train(self) -> str:
        """
        :return: {ai}/classification/lda/train
        """
        return f"{self.classification()}/lda/train"

    def classification_predict(self) -> str:
        """
        :return: {ai}/classification/predict
        """
        return f"{self.classification()}/predict"

    def clustering(self) -> str:
        """
        :return: {ai}/clustering
        """
        return f"{self.ai()}/clustering"

    def clustering_kmeans_train(self) -> str:
        """
        :return: {ai}/clustering/kmeans/train
        """
        return f"{self.clustering()}/kmeans/train"

    def clustering_predict(self) -> str:
        """
        :return: {ai}/clustering/predict
        """
        return f"{self.clustering()}/predict"

    def construct_ai(self, route_name: str) -> str:
        """
        :return: {ai}/{route_name}
        """
        return f"{self.ai()}/{route_name}"

    def construct_ai_instructions(self, route_name: str) -> str:
        """
        :return: {ai}/{route_name}/instructions
        """
        return f"{self.ai()}/{route_name}/instructions"

    def check_if_route_is_available(self, route_name: str) -> bool:
        """
        :return: if route is available in specific list
        """
        return f"{self.ai()}/{route_name}" in [
            self.regression_svr_train(),
            self.regression_predict(),
            self.classification_svc_train(),
            self.classification_lda_train(),
            self.classification_predict(),
            self.clustering_kmeans_train(),
            self.clustering_predict(),
        ]


class Api(BaseApi):
    def get_healthcheck(self) -> dict:
        return self._response_wrapper(self.session.get(self.router.healthcheck()))

    def post_(self, route_name: str, data: dict) -> dict:
        return self._response_wrapper(
            self.session.post(self.router.construct_ai(route_name), json=data)
        )

    def get_instructions_for_(self, route_name: str) -> dict:
        return self._response_wrapper(
            self.session.get(self.router.construct_ai_instructions(route_name))
        )

    def get_base_save_path(self) -> dict:
        return self._response_wrapper(self.session.get(self.router.base_save_path()))


client = Api(Router, AI_API_BASE_URL)
