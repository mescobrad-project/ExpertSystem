from typing import Any
from sqlalchemy.orm import Session
from src.schemas.NewWorkflowSchema import WorkflowBase, WorkflowStepBase
import uuid
from src.models._all import (
    NewWorkflowModel,
    NewWorkflowStepModel,
    NewWorkflowActionModel,
    NewWorkflowActionConditionalModel,
    NewRunModel
)
from src.services.NewRunService import delete_run


def createWorkflow(db: Session, workflow_in: WorkflowBase, ws_id: int) -> WorkflowBase:
    """
    Create a new workflow with its metadata.
    """
    workflow = {
        "id": uuid.uuid4(),
        "name": workflow_in.name,
        "description": workflow_in.description,
        "category_id": workflow_in.category_id,
        "is_template": workflow_in.is_template,
        "is_part_of_other": workflow_in.is_part_of_other,
        "json_representation": workflow_in.json_representation,
        "ws_id": ws_id,
    }
    try:
        db.execute(NewWorkflowModel.__table__.insert().values(workflow))
        print(workflow["id"])
    except Exception as e:
        db.rollback()
        raise e
    steps = workflow_in.steps
    for step_in in steps:
        step_in.workflow_id = workflow["id"]
        step = {
            "id": uuid.uuid4(),
            "name": step_in.name,
            "description": step_in.description,
            "workflow_id": workflow["id"],
            "order": step_in.order,
            "ws_id": ws_id,
        }
        db.execute(NewWorkflowStepModel.__table__.insert().values(step))
        for action_in in step_in.actions:
            action_in.step_id = step["id"]
            action = {
                "id": uuid.uuid4(),
                "name": action_in.name,
                "description": action_in.description,
                "workflow_step_id": step["id"],
                "ws_id": ws_id,
                "action_type": action_in.action_type,
                "order": action_in.order,
                "action": action_in.action,
                "is_conditional": action_in.is_conditional,
                "weight_to_true": action_in.weight_to_true,
                "method": action_in.method,
                "input": action_in.input,
            }
            db.execute(NewWorkflowActionModel.__table__.insert().values(action))
            if action_in.is_conditional:
                for conditional_in in action_in.conditions:
                    conditional = {
                        "id": uuid.uuid4(),
                        "workflow_action_id": action["id"],
                        "ws_id": ws_id,
                        "variable": conditional_in.variable,
                        "value": conditional_in.value,
                        "weight": conditional_in.weight,
                        "metadata_value": conditional_in.metadata_value,
                        "condition": conditional_in.condition,
                        "order": conditional_in.order,
                    }
                    db.execute(
                        NewWorkflowActionConditionalModel.__table__.insert().values(
                            conditional
                        )
                    )
    db.commit()
    return workflow["id"]


def getWorkflows(
    db: Session,
    ws_id: int,
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
    workflows = (
        db.query(NewWorkflowModel)
        .filter(
            NewWorkflowModel.ws_id == ws_id
            and NewWorkflowModel.is_template == is_template
        )
        .slice(skip, limit)
        .all()
    )
    for w in workflows:
        steps = (
            db.query(NewWorkflowStepModel)
            .filter(NewWorkflowStepModel.workflow_id == str(w.id))
            .all()
        )
        for s in steps:
            actions = (
                db.query(NewWorkflowActionModel)
                .filter(NewWorkflowActionModel.workflow_step_id == str(s.id))
                .all()
            )
            for a in actions:
                conditionals = (
                    db.query(NewWorkflowActionConditionalModel)
                    .filter(
                        NewWorkflowActionConditionalModel.workflow_action_id
                        == str(a.id)
                    )
                    .all()
                )
                a.conditionals = conditionals
            s.actions = actions
        w.steps = steps
    return {
        "data": workflows,
        "paging": {
            "previous_link": f"/v2/workflow?skip={skip - limit}&limit={limit}&category={category}&is_template={is_template}&order={order}&direction={direction}",
            "next_link": f"/v2/workflow?skip={skip + limit}&limit={limit}&category={category}&is_template={is_template}&order={order}&direction={direction}",
            "count": db.query(NewWorkflowModel)
            .filter(
                NewWorkflowModel.ws_id == ws_id
                and NewWorkflowModel.is_template == is_template
            )
            .count(),
        },
    }


def getWorkflow(db: Session, ws_id: int, workflow_id: uuid.UUID) -> WorkflowBase:
    """
    Retrieve a workflow with its metadata.
    """
    workflow = (
        db.query(NewWorkflowModel)
        .filter(NewWorkflowModel.id == workflow_id and NewWorkflowModel.ws_id == ws_id)
        .first()
    )
    steps = (
        db.query(NewWorkflowStepModel)
        .filter(NewWorkflowStepModel.workflow_id == workflow_id)
        .all()
    )
    for s in steps:
        actions = (
            db.query(NewWorkflowActionModel)
            .filter(NewWorkflowActionModel.step_id == s.id)
            .all()
        )
        for a in actions:
            conditionals = (
                db.query(NewWorkflowActionConditionalModel)
                .filter(NewWorkflowActionConditionalModel.action_id == a.id)
                .all()
            )
            a.conditional = conditionals
        s.actions = actions
    workflow.steps = steps
    return workflow


def addStep(db: Session, step_in: WorkflowStepBase, ws_id: int) -> WorkflowStepBase:
    """
    Add a step to a workflow.
    """
    step = {
        "id": uuid.uuid4(),
        "name": step_in.name,
        "description": step_in.description,
        "workflow_id": step_in.workflow_id,
        "order": step_in.order,
        "ws_id": ws_id,
    }
    db.execute(NewWorkflowStepModel.__table__.insert().values(step))
    return step


def addAction(
    db: Session, action_in: NewWorkflowActionModel, ws_id: int
) -> NewWorkflowActionModel:
    """
    Add an action to a step.
    """
    action = {
        "id": uuid.uuid4(),
        "name": action_in.name,
        "description": action_in.description,
        "workflow_step_id": action_in.step_id,
        "ws_id": ws_id,
        "order": action_in.order,
        "action": action_in.action_type,
        "is_conditional": action_in.is_conditional,
        "weight_to_true": action_in.weight_to_true,
    }
    db.execute(NewWorkflowActionModel.__table__.insert().values(action))
    if action_in.is_conditional:
        for conditional_in in action_in.conditions:
            conditional = {
                "id": uuid.uuid4(),
                "workflow_action_id": action["id"],
                "ws_id": ws_id,
                "variable": conditional_in.variable,
                "value": conditional_in.value,
                "weight": conditional_in.weight,
                "metadata_value": conditional_in.metadata_value,
                "order": conditional_in.order,
            }
            db.execute(
                NewWorkflowActionConditionalModel.__table__.insert().values(conditional)
            )
    return action

def deleteWorkflow(db: Session, workflow_id: uuid.UUID) -> Any:
    """
    Delete a workflow with its metadata.
    """
    try:
        runs = db.query(NewRunModel).filter(NewRunModel.workflow_id == str(workflow_id)).all()
        for r in runs:
            delete_run(db, r.id)
        steps = db.query(NewWorkflowStepModel).filter(NewWorkflowStepModel.workflow_id == str(workflow_id)).all()
        for step in steps:
            actions = db.query(NewWorkflowActionModel).filter(NewWorkflowActionModel.workflow_step_id == str(step.id)).all()
            for action in actions:
                conditionals = db.query(NewWorkflowActionConditionalModel).filter(NewWorkflowActionConditionalModel.workflow_action_id == str(action.id)).all()
                for conditional in conditionals:
                    db.execute(
                        NewWorkflowActionConditionalModel.__table__.delete().where(
                            NewWorkflowActionConditionalModel.id == str(conditional.id)
                        )
                    )
                db.execute(
                    NewWorkflowActionModel.__table__.delete().where(
                        NewWorkflowActionModel.id == str(action.id)
                    )
                )
            db.execute(
                NewWorkflowStepModel.__table__.delete().where(
                    NewWorkflowStepModel.id == str(step.id)
                )
            )
        db.execute(
            NewWorkflowModel.__table__.delete().where(
                NewWorkflowModel.id == str(workflow_id)
            )
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    return {"message": "Workflow deleted."}
