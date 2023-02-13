from src.repositories.FeatureRepository import FeatureRepository
from ._base import BaseController


class _FeatureController(BaseController):
    pass


FeatureController = _FeatureController(FeatureRepository)
