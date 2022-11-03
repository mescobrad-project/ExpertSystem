from sqlalchemy.orm import Session

from src.controllers.WorkflowController import WorkflowController
from src.models.WorkflowModel import WorkflowModel
from src.schemas.WorkflowSchema import WorkflowCreate, WorkflowUpdate
from ._base import random_lower_string, random_unique_string, random_dict_obj
from .WorkflowCategoryUtils import seed_category


def create_random_workflow() -> tuple[str, dict]:
    name = random_unique_string()
    description = random_lower_string()
    tasks = random_dict_obj()
    raw_diagram_data = random_dict_obj()

    return name, description, tasks, raw_diagram_data


def seed_workflow(db: Session) -> dict[str, dict, WorkflowModel]:
    name, description, tasks, raw_diagram_data = create_random_workflow()
    category = seed_category(db)

    workflow_in = WorkflowCreate(
        category_id=category["obj"].id,
        name=name,
        description=description,
        tasks=tasks,
        raw_diagram_data=raw_diagram_data,
    )
    return {
        "category_id": category["obj"].id,
        "name": name,
        "description": description,
        "tasks": tasks,
        "raw_diagram_data": raw_diagram_data,
        "obj": WorkflowController.create(db=db, obj_in=workflow_in),
    }


def update_seed_workflow(
    db: Session, workflow: WorkflowModel
) -> dict[str, dict, WorkflowModel]:
    _, description, tasks, raw_diagram_data = create_random_workflow()

    workflow_update = WorkflowUpdate(
        description=description, tasks=tasks, raw_diagram_data=raw_diagram_data
    )
    return {
        "description": description,
        "tasks": tasks,
        "raw_diagram_data": raw_diagram_data,
        "obj": WorkflowController.update(
            db=db, db_obj=workflow, obj_in=workflow_update
        ),
    }


def remove_workflow(
    db: Session, workflow: WorkflowModel
) -> tuple[WorkflowModel | None]:
    _ = WorkflowController.remove(db=db, id=workflow.id)
    try:
        workflow_validated = WorkflowController.get(db=db, id=workflow.id)
    except:
        workflow_validated = None

    return workflow_validated
