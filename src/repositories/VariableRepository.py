from ._base import BaseCRUD
from src.models._all import VariableModel
from src.schemas.VariableSchema import VariableCreate, VariableUpdate


class _VariableRepository(BaseCRUD[VariableModel, VariableCreate, VariableUpdate]):
    pass


VariableRepository = _VariableRepository(VariableModel)
