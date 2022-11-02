from ._base import CRUDBase
from src.models._all import ModuleCategoryModel
from src.schemas.ModuleCategorySchema import ModuleCategoryCreate, ModuleCategoryUpdate


class CRUDModuleCategory(
    CRUDBase[ModuleCategoryModel, ModuleCategoryCreate, ModuleCategoryUpdate]
):
    pass


ModuleCategoryController = CRUDModuleCategory(ModuleCategoryModel)
