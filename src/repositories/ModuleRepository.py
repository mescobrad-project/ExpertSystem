from ._base import BaseCRUD
from src.models._all import ModuleModel
from src.schemas.ModuleSchema import ModuleCreate, ModuleUpdate


class _ModuleRepository(BaseCRUD[ModuleModel, ModuleCreate, ModuleUpdate]):
    pass


ModuleRepository = _ModuleRepository(ModuleModel)
