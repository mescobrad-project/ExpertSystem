from ._base import BaseCRUD
from src.models._all import PlatformUserDefaultWorkspaceModel
from src.schemas.PlatformUserDefaultWorkspaceSchema import (
    PlatformUserDefaultWorkspaceCreate,
    PlatformUserDefaultWorkspaceUpdate,
)


class _PlatformUserDefaultWorkspaceRepository(
    BaseCRUD[
        PlatformUserDefaultWorkspaceModel,
        PlatformUserDefaultWorkspaceCreate,
        PlatformUserDefaultWorkspaceUpdate,
    ]
):
    pass


PlatformUserDefaultWorkspaceRepository = _PlatformUserDefaultWorkspaceRepository(
    PlatformUserDefaultWorkspaceModel
)
