from src.repositories.ModuleCategoryRepository import ModuleCategoryRepository
from ._base import BaseController


class _ModuleCategoryController(BaseController):
    pass


ModuleCategoryController = _ModuleCategoryController(ModuleCategoryRepository)
