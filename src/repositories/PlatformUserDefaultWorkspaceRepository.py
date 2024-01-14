from sqlalchemy.orm import Session
from ._base import BaseCRUD
from src.models._all import PlatformUserDefaultWorkspaceModel
from src.repositories._base import _parse_criteria
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
    def get_multi(
        self,
        db: Session,
        *,
        criteria={},
    ) -> list[PlatformUserDefaultWorkspaceModel]:
        return db.query(self.model).filter(*_parse_criteria(self.model, criteria)).all()


PlatformUserDefaultWorkspaceRepository = _PlatformUserDefaultWorkspaceRepository(
    PlatformUserDefaultWorkspaceModel
)
