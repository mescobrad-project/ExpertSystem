from ._base import CRUDBase
from src.models._all import ModuleModel
from src.schemas.ModuleSchema import ModuleCreate, ModuleUpdate


class CRUDModule(CRUDBase[ModuleModel, ModuleCreate, ModuleUpdate]):
    pass


ModuleController = CRUDModule(ModuleModel)
