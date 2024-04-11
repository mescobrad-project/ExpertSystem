from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.errors.ApiRequestException import (
    InternalServerErrorException,
    NotFoundException,
)
from src.models._all import PlatformWorkspaceModel
from src.repositories.PlatformUserDefaultWorkspaceRepository import (
    PlatformUserDefaultWorkspaceRepository,
)
from src.utils.pagination import append_query_in_uri
from ._base import BaseController


class _PlatformUserDefaultWorkspaceController(BaseController):
    def read_multi(self, db: Session, criteria: dict = {}):
        try:
            return [
                def_workspace.workspace
                for def_workspace in self.repository.get_multi(db, criteria=criteria)
            ]
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))

    def read_by_ws_id(self, db: Session, ws_id: int, criteria: dict = {}):
        criteria["ws_id"] = ws_id

        data = self.repository.get_one(db=db, criteria=criteria)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data


PlatformUserDefaultWorkspaceController = _PlatformUserDefaultWorkspaceController(
    PlatformUserDefaultWorkspaceRepository
)
