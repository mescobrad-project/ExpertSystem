from ._base import BaseCRUD
from src.models._all import PlatformWorkspaceModel
from src.schemas.PlatformWorkspaceSchema import (
    PlatformWorkspaceCreate,
    PlatformWorkspaceUpdate,
)


class _PlatformWorkspaceRepository(
    BaseCRUD[PlatformWorkspaceModel, PlatformWorkspaceCreate, PlatformWorkspaceUpdate]
):
    pass


PlatformWorkspaceRepository = _PlatformWorkspaceRepository(PlatformWorkspaceModel)
