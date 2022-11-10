from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from src.database import get_db
from src.models.WorkflowModel import WorkflowModel
from src.models.ModuleCategoryModel import ModuleCategoryModel
from src.controllers.WorkflowController import WorkflowController
from src.schemas.WorkflowSchema import Workflow, WorkflowCreate, WorkflowUpdate
from src.controllers.RunController import RunController
from src.schemas.RunSchema import Run
from src.utils.pagination import append_query_in_uri
from ._base import RouteHelper

router = APIRouter(
    prefix="/workflow", tags=["workflow"], responses={404: {"message": "Not found"}}
)

route_helper = RouteHelper(WorkflowController)
run_route_helper = RouteHelper(RunController)


@router.get("", response_model=dict[str, Any | list[Workflow]])
def read_workflows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    is_template: bool = False,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve workflows with their metadata.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    criteria = {}
    if category:
        criteria["category"] = {
            "model": ModuleCategoryModel,
            "criteria": {"code": category},
        }

    criteria["is_template"] = is_template

    criteria["deleted_at"] = None

    response = route_helper.read_multi(db, skip, limit, order, direction, criteria)

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


@router.post("")
def create_workflow(
    *, db: Session = Depends(get_db), workflow_in: WorkflowCreate
) -> Any:
    """
    Create new workflow.
    """
    try:
        workflow = WorkflowController.create(db=db, obj_in=workflow_in)

        workflow_upd = WorkflowUpdate()
        [tasks, stores] = WorkflowController.parse_xml(
            workflow.raw_diagram_data["xml_original"]
        )
        workflow_upd.tasks = tasks
        workflow_upd.stores = stores
        workflow = WorkflowController.update(
            db=db, db_obj=workflow, obj_in=workflow_upd
        )
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Workflow already exists")
    except Exception:
        raise HTTPException(status_code=400, detail="Provided input is wrong")

    return workflow


@router.get("/entity_types")
def read_entity_types() -> Any:
    """
    Get all available workflow entity types.
    """
    entity_types = WorkflowController.get_workflow_entity_types()
    if not entity_types:
        raise HTTPException(status_code=404, detail="Entities not found")

    return entity_types


@router.get("/deleted", response_model=dict[str, Any | list[Workflow]])
def read_deleted_workflows(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    is_template: bool = False,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve deleted workflows.
    Params explain:
    order: The model's prop as str, e.g. id
    direction: asc | desc
    """
    criteria = {}
    if category:
        criteria["category"] = {
            "model": ModuleCategoryModel,
            "criteria": {"code": category},
        }

    criteria["is_template"] = is_template

    criteria["deleted_at__not"] = None

    response = route_helper.read_multi(db, skip, limit, order, direction, criteria)

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


@router.get("/deleted/{workflow_id}", response_model=Workflow)
def read_deleted_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get deleted workflow by ID.
    """
    return route_helper.read(workflow_id, db=db, criteria={"deleted_at__not": None})


@router.get("/{workflow_id}", response_model=Workflow)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Get workflow by ID.
    """
    return route_helper.read(workflow_id, db=db, criteria={"deleted_at": None})


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
    workflow_in: WorkflowUpdate,
) -> Any:
    """
    Update a workflow.
    """
    workflow = route_helper.read(workflow_id, db=db, criteria={"deleted_at": None})

    [tasks, stores] = WorkflowController.parse_xml(
        workflow.raw_diagram_data["xml_original"]
    )
    workflow_in.tasks = tasks
    workflow_in.stores = stores
    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.delete("/{workflow_id}", response_model=Workflow)
def destroy_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Delete a workflow.
    """
    workflow = route_helper.read(workflow_id, db=db, criteria={"deleted_at": None})

    if workflow.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow already destroyed")

    workflow_in = WorkflowUpdate()
    workflow_in.deleted_at = datetime.now(tz=timezone.utc)
    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.delete("/{workflow_id}/revert", response_model=Workflow)
def revert_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow.
    """
    workflow = route_helper.read(workflow_id, db=db, criteria={"deleted_at__not": None})

    if not workflow.deleted_at:
        raise HTTPException(status_code=405, detail="Workflow is active")

    workflow_in = WorkflowUpdate()
    workflow_in.deleted_at = None
    workflow = WorkflowController.update(db=db, db_obj=workflow, obj_in=workflow_in)
    return workflow


@router.get("/{workflow_id}/task/{task_name}")
def read_task_details(
    *, db: Session = Depends(get_db), workflow_id: UUID, task_name: str
) -> Any:
    """
    Get task details given its name and workflow ID.
    """
    workflow = route_helper.read(workflow_id, db=db, criteria={"deleted_at": None})

    for key, task in workflow.tasks.items():
        if key == task_name:
            return task

    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/{workflow_id}/run", response_model=dict[str, Any | list[Run]])
def read_workflow_runs(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve running instances of specific workflow.
    """
    return run_route_helper.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        {
            "workflow_id": workflow_id,
            "workflow": {"model": WorkflowModel, "criteria": {"deleted_at": None}},
        },
    )
