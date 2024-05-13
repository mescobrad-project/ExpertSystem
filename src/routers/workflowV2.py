from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from src.models._all import WorkflowModel
from src.controllers.WorkflowController import WorkflowController
from src.schemas.WorkflowSchema import (
    Workflow,
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowWorkspaceChange,
)
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user, get_user_only
from src.dependencies.workspace import validate_workspace
from src.schemas.RunSchema import Run

from src.models._all import NewWorkflowModel, NewWorkflowStepModel, NewWorkflowActionModel, NewWorkflowActionConditionalModel

router = APIRouter(
    prefix="/v2/workflow",
    tags=["workflow"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.get("/", response_model=dict[str, Any | list[Workflow]])
def read_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
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
    
    workflows = db.query(NewWorkflowModel).filter(NewWorkflowModel.ws_id == ws_id and NewWorkflowModel.is_template == is_template).slice(skip, limit).all()
    for w in workflows:
        steps = db.query(NewWorkflowStepModel).filter(NewWorkflowStepModel.workflow_id == w.id).all()
        for s in steps:
            actions = db.query(NewWorkflowActionModel).filter(NewWorkflowActionModel.step_id == s.id).all()
            for a in actions:
                conditionals = db.query(NewWorkflowActionConditionalModel).filter(NewWorkflowActionConditionalModel.action_id == a.id).all()
                a.conditional = conditionals
            s.actions = actions
        w.steps = steps
    return {'data': workflows, 
                'paging': {'previous_link': f'/v2/workflow?skip={skip - limit}&limit={limit}&category={category}&is_template={is_template}&order={order}&direction={direction}',
                'next_link': f'/v2/workflow?skip={skip + limit}&limit={limit}&category={category}&is_template={is_template}&order={order}&direction={direction}'}
    }


@router.post("/")
def create_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_in: Any,
) -> Any:
    """
    Create new workflow.
    """
    
    workflow = {
        "name": workflow_in.name,
        "description": workflow_in.description,
        "category": workflow_in.category,
        "is_template": workflow_in.is_template,
        "is_part_of_other": step_in.is_part_of_other,
        "json_representation": workflow_in.json_representation,
        "ws_id": ws_id,
    }
    db.begin()
    workflow = db.execute(NewWorkflowModel.__table__.insert().values(workflow))
    print(workflow.id)
    steps = workflow_in.steps
    for step_in in steps:
        step_in['workflow_id'] = workflow.id
        step = {
            "name": step_in.name,
            "description": step_in.description,
            "workflow_id": workflow.id,
            "order": step_in.order,
            "ws_id": ws_id
        }
        step = db.execute(NewWorkflowStepModel.__table__.insert().values(step))
        for action_in in step_in.actions:
            action_in['step_id'] = step.id
            action = {
                "name": action_in.name,
                "description": action_in.description,
                "step_id": step.id,
                "ws_id": ws_id,
                "order": action_in.order,
                "action_type": action_in.action_type,
                "is_conditional": action_in.is_conditional,
                "weight_to_true": action_in.weight_to_true
            }
            action = db.execute(NewWorkflowActionModel.__table__.insert().values(action))
            if action_in.conditional:
                conditional = {
                    "action_id": action.id,
                    "ws_id": ws_id,
                    "variable": action_in.conditional['variable'],
                    "value": action_in.conditional['value'],
                    "weight": action_in.conditional['weight'],
                    "metadata": action_in.conditional['metadata'],
                    "order": action_in.conditional['order']
                }
                db.execute(NewWorkflowActionConditionalModel.__table__.insert().values(conditional))
    db.commit()
        

@router.get("/deleted", response_model=dict[str, Any | list[Workflow]])
def read_deleted_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
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
    return WorkflowController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        is_template,
        category,
        criteria={"deleted_at__not": None, "ws_id": ws_id},
    )


@router.get("/deleted/{workflow_id}", response_model=Workflow)
def read_deleted_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_id: UUID,
) -> Any:
    """
    Get deleted workflow by ID.
    """
    return WorkflowController.read(
        db=db,
        resource_id=workflow_id,
        criteria={"deleted_at__not": None, "ws_id": ws_id},
    )


@router.get("/search", response_model=Workflow)
def search_workflows(
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    name: str = None,
) -> Any:
    """
    Retrieve a workflow using search params.
    """
    return WorkflowController.search(
        db,
        params={"name": name},
        criteria={"deleted_at": None, "is_template": False, "ws_id": ws_id},
    )


@router.get("/{workflow_id}", response_model=Workflow)
def read_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_id: UUID,
) -> Any:
    """
    Get workflow by ID.
    """
    return WorkflowController.read(
        db=db, resource_id=workflow_id, criteria={"deleted_at": None, "ws_id": ws_id}
    )


@router.put("/{workflow_id}", response_model=Workflow)
def update_workflow(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_id: UUID,
    workflow_in: WorkflowUpdate,
) -> Any:
    """
    Update a workflow.
    """
    workflow_in.ws_id = ws_id

    return WorkflowController.update(
        db=db, resource_id=workflow_id, resource_in=workflow_in
    )


@router.put("/{workflow_id}/workspace", response_model=int)
def change_workspace(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    user: int = Depends(get_user_only),
    workflow_id: UUID,
    workflow_in: WorkflowWorkspaceChange,
) -> Any:
    """
    Change the workspace of a workflow.
    """
    return RunController.change_workspace(
        db=db,
        resource_id=workflow_id,
        user_name=user.info["preferred_username"],
        ws_id=workflow_in.ws_id,
    )


@router.delete("/{workflow_id}", response_model=Workflow)
def destroy_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Delete a workflow.
    """
    return WorkflowController.destroy(
        db=db, resource_id=workflow_id, resource_in=WorkflowUpdate()
    )


@router.delete("/{workflow_id}/revert", response_model=Workflow)
def revert_workflow(
    *,
    db: Session = Depends(get_db),
    workflow_id: UUID,
) -> Any:
    """
    Revert the deletion of a workflow.
    """
    return WorkflowController.revert(
        db=db, resource_id=workflow_id, resource_in=WorkflowUpdate()
    )


@router.get("/{workflow_id}/task/{task_sid}")
def read_task_details(
    *, db: Session = Depends(get_db), workflow_id: UUID, task_sid: str
) -> Any:
    """
    Get task details given its SID (e.g. Activity_04n854t) and workflow ID.
    """
    return WorkflowController.read_task_details(
        db=db, resource_id=workflow_id, task_sid=task_sid
    )


@router.get("/{workflow_id}/run", response_model=dict[str, Any | list[Run]])
def read_workflow_runs(
    *,
    db: Session = Depends(get_db),
    ws_id: int = 1, #Depends(validate_workspace),
    workflow_id: UUID,
    skip: int = 0,
    limit: int = 100,
    order: str = None,
    direction: str = None,
) -> Any:
    """
    Retrieve running instances of specific workflow.
    """
    return RunController.read_multi(
        db,
        skip,
        limit,
        order,
        direction,
        {
            "workflow_id": workflow_id,
            "workflow": {
                "model": WorkflowModel,
                "criteria": {"deleted_at": None, "ws_id": ws_id},
            },
            "ws_id": ws_id,
        },
    )
