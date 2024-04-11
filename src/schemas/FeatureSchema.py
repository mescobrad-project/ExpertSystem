from ._association import FeatureBase, FeatureInDBBase


# Properties to receive on obj creation
class FeatureCreate(FeatureBase):
    name: str


# Properties to receive on obj update
class FeatureUpdate(FeatureBase):
    pass


# Properties to return to client
class Feature(FeatureInDBBase):
    pass


# Properties stored in DB
class FeatureInDB(FeatureInDBBase):
    pass
