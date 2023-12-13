from sqlalchemy.orm import Session
from src.errors.ApiRequestException import NotFoundException
from src.repositories.PlatformWorkspaceRepository import (
    PlatformWorkspaceRepository,
)
from ._base import BaseController


class _PlatformWorkspaceController(BaseController):
    def read(self, db: Session, ws_id: int, criteria: dict = {}):
        criteria["ws_id"] = ws_id

        data = self.repository.get_one(db=db, criteria=criteria)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data


PlatformWorkspaceController = _PlatformWorkspaceController(PlatformWorkspaceRepository)
