from sqlalchemy.orm import Session

from src.controllers.WorkflowController import WorkflowController
from src.tests.utils._base import check_if_dicts_match
from src.tests.utils.WorkflowUtils import (
    seed_workflow,
    remove_workflow,
    update_seed_workflow,
)


def test_create_workflow(db: Session) -> None:
    workflow = seed_workflow(db)

    assert workflow["obj"].category_id == workflow["category_id"]
    assert workflow["obj"].name == workflow["name"]
    assert workflow["obj"].description == workflow["description"]
    assert workflow["obj"].is_template == workflow["is_template"]
    assert check_if_dicts_match(workflow["obj"].tasks, workflow["tasks"])
    assert check_if_dicts_match(
        workflow["obj"].raw_diagram_data, workflow["raw_diagram_data"]
    )


def test_get_workflow(db: Session) -> None:
    workflow = seed_workflow(db)

    stored = WorkflowController.read(
        db=db, resource_id=workflow["obj"].id, criteria={"deleted_at": None}
    )
    assert stored
    assert workflow["obj"].category_id == stored.category_id
    assert workflow["obj"].name == stored.name
    assert workflow["obj"].description == stored.description
    assert workflow["obj"].is_template == stored.is_template
    assert check_if_dicts_match(workflow["obj"].tasks, stored.tasks)
    assert check_if_dicts_match(
        workflow["obj"].raw_diagram_data, stored.raw_diagram_data
    )


def test_update_workflow(db: Session) -> None:
    workflow1 = seed_workflow(db)
    workflow2 = update_seed_workflow(db, workflow1["obj"].id)

    assert workflow2["obj"].description == workflow2["description"]
    assert workflow2["obj"].is_template == workflow2["is_template"]
    assert check_if_dicts_match(workflow2["obj"].tasks, workflow2["tasks"])
    assert check_if_dicts_match(
        workflow2["obj"].raw_diagram_data, workflow2["raw_diagram_data"]
    )


def test_delete_workflow(db: Session) -> None:
    workflow = seed_workflow(db)
    workflow_validate = remove_workflow(db, workflow["obj"].id)

    assert workflow_validate is None
