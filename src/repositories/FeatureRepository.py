from ._base import BaseCRUD
from src.models._all import FeatureModel
from src.schemas.FeatureSchema import FeatureCreate, FeatureUpdate


class _FeatureRepository(BaseCRUD[FeatureModel, FeatureCreate, FeatureUpdate]):
    pass


FeatureRepository = _FeatureRepository(FeatureModel)
