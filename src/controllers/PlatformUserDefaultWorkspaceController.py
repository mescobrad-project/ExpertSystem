from sqlalchemy.orm import Session
from src.errors.ApiRequestException import NotFoundException
from src.models._all import PlatformWorkspaceModel
from src.repositories.PlatformUserDefaultWorkspaceRepository import (
    PlatformUserDefaultWorkspaceRepository,
)
from src.utils.pagination import append_query_in_uri
from ._base import BaseController


class _PlatformUserDefaultWorkspaceController(BaseController):
    def read_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order: str = None,
        direction: str = None,
        ws_id: int = None,
        criteria: dict = {},
    ):
        if ws_id:
            criteria["ws_id"] = {
                "model": PlatformWorkspaceModel,
                "criteria": {"ws_id": ws_id},
            }

        response = super().read_multi(db, skip, limit, order, direction, criteria)

        if ws_id != None:
            response["paging"]["previous_link"] = append_query_in_uri(
                response["paging"]["previous_link"], f"wsid={ws_id}"
            )
            response["paging"]["next_link"] = append_query_in_uri(
                response["paging"]["next_link"], f"wsid={ws_id}"
            )

        return response

    def read_by_ws_id(self, db: Session, ws_id: int, criteria: dict = {}):
        criteria["ws_id"] = ws_id

        data = self.repository.get_one(db=db, criteria=criteria)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data


PlatformUserDefaultWorkspaceController = _PlatformUserDefaultWorkspaceController(
    PlatformUserDefaultWorkspaceRepository
)
