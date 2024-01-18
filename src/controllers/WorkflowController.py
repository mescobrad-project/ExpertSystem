from uuid import UUID
from sqlalchemy.orm import Session
from src.errors.ApiRequestException import NotFoundException
from src.models._all import WorkflowCategoryModel
from src.repositories.WorkflowRepository import WorkflowRepository
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate
from src.utils.pagination import append_query_in_uri
from src.utils.workflow import get_workflow_entity_types, parse_xml
from ._base import BaseController


def _handle_additional_task_settings(tasks, settings):
    for task in settings:
        if task in tasks.keys():
            tasks[task]["default"] = settings[task].get("default")
        else:
            for t in tasks:
                if (
                    tasks[t].get("class")
                    and settings[task].get("class")
                    and settings[task]["class"][0] == tasks[t]["class"][0]
                ):
                    tasks[task]["default"] = settings[task].get("default")


class _WorkflowController(BaseController):
    def read_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order: str = None,
        direction: str = None,
        is_template: bool = False,
        category: str = None,
        criteria: dict = {},
    ):
        if category:
            criteria["category"] = {
                "model": WorkflowCategoryModel,
                "criteria": {"code": category},
            }

        criteria["is_template"] = is_template

        response = super().read_multi(db, skip, limit, order, direction, criteria)

        if category != None:
            response["paging"]["previous_link"] = append_query_in_uri(
                response["paging"]["previous_link"], f"category={category}"
            )
            response["paging"]["next_link"] = append_query_in_uri(
                response["paging"]["next_link"], f"category={category}"
            )

        if is_template:
            response["paging"]["previous_link"] = append_query_in_uri(
                response["paging"]["previous_link"], f"is_template={is_template}"
            )
            response["paging"]["next_link"] = append_query_in_uri(
                response["paging"]["next_link"], f"is_template={is_template}"
            )

        return response

    def search(
        self,
        db: Session,
        params: dict = {},
        criteria: dict = {},
    ):
        if params.get("name"):
            criteria["name"] = params.get("name")

        data = self.repository.get_one(db=db, criteria=criteria)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data

    def read_entity_types(self):
        return get_workflow_entity_types()

    def create(self, db: Session, *, obj_in: WorkflowCreate):
        settings = obj_in.settings
        del obj_in.settings

        workflow = super().create(db, obj_in=obj_in)

        [tasks, stores] = parse_xml(workflow.raw_diagram_data["xml_original"])
        workflow_upd = WorkflowUpdate()

        _handle_additional_task_settings(tasks, settings)
        workflow_upd.tasks = tasks

        workflow_upd.stores = stores

        return super().update(db=db, resource_id=workflow.id, resource_in=workflow_upd)

    def update(
        self,
        db: Session,
        resource_id: UUID,
        resource_in: WorkflowUpdate,
        criteria: any = {"deleted_at": None},
    ):
        settings = resource_in.settings
        resource_in.settings = None

        if resource_in.raw_diagram_data and resource_in.raw_diagram_data.get(
            "xml_original"
        ):
            raw_diagram = resource_in.raw_diagram_data.get("xml_original")
        else:
            workflow = super().read(db=db, resource_id=resource_id, criteria=criteria)
            raw_diagram = workflow.raw_diagram_data["xml_original"]

        [tasks, stores] = parse_xml(raw_diagram)

        _handle_additional_task_settings(tasks, settings)
        resource_in.tasks = tasks
        resource_in.stores = stores

        return super().update(
            db=db, resource_id=resource_id, resource_in=resource_in, criteria=criteria
        )

    def update_workspace(
        self,
        db: Session,
        resource_id: UUID,
        ws_id: int,
        criteria: any = {"deleted_at": None},
    ):
        return super().update(
            db=db,
            resource_id=resource_id,
            resource_in=WorkflowUpdate(ws_id=ws_id),
            criteria=criteria,
        )

    def read_task_details(self, db: Session, resource_id: UUID, task_sid: str):
        workflow = super().read(
            db=db, resource_id=resource_id, criteria={"deleted_at": None}
        )

        for key, task in workflow.tasks.items():
            if key == task_sid:
                return task

        raise NotFoundException(details="Task not found in workflow")


WorkflowController = _WorkflowController(WorkflowRepository)
