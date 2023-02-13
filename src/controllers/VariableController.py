from src.repositories.VariableRepository import VariableRepository
from ._base import BaseController


class _VariableController(BaseController):
    pass


VariableController = _VariableController(VariableRepository)
