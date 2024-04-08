from sqlalchemy.orm import Session
from src.models._all import ModuleCategoryModel
from src.repositories.ModuleRepository import ModuleRepository
from src.utils.pagination import append_query_in_uri
from ._base import BaseController


class _ModuleController(BaseController):
    def read_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order: str = None,
        direction: str = None,
        task: str = None,
        category: str = None,
        criteria: dict = {},
    ):
        if category:
            criteria["category"] = {
                "model": ModuleCategoryModel,
                "criteria": {"code": category},
            }

        if task:
            criteria["task"] = task

        response = super().read_multi(db, skip, limit, order, direction, criteria)

        if category != None:
            response["paging"]["previous_link"] = append_query_in_uri(
                response["paging"]["previous_link"], f"category={category}"
            )
            response["paging"]["next_link"] = append_query_in_uri(
                response["paging"]["next_link"], f"category={category}"
            )

        if task != None:
            response["paging"]["previous_link"] = append_query_in_uri(
                response["paging"]["previous_link"], f"task={task}"
            )
            response["paging"]["next_link"] = append_query_in_uri(
                response["paging"]["next_link"], f"task={task}"
            )

        return response


ModuleController = _ModuleController(ModuleRepository)
