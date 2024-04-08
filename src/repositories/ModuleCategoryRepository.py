from ._base import BaseCRUD
from src.models._all import ModuleCategoryModel
from src.schemas.ModuleCategorySchema import ModuleCategoryCreate, ModuleCategoryUpdate


class _ModuleCategoryRepository(
    BaseCRUD[ModuleCategoryModel, ModuleCategoryCreate, ModuleCategoryUpdate]
):
    pass


ModuleCategoryRepository = _ModuleCategoryRepository(ModuleCategoryModel)
