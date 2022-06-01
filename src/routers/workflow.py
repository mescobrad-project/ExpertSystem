from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.WorkflowController import WorkflowController
from src.models._all import WorkflowModel
from src.schemas.WorkflowSchema import Workflow

router = APIRouter(
    prefix="", tags=["workflow"], responses={404: {"message": "Not found"}}
)


# @router.post("/", response_model=WorkflowBase.Workflow)
# def create_workflow(workflow: WorkflowBase.Workflow, db: Session = Depends(get_db)):
#     db_workflow = read_by_name(db, name=workflow.name)
#     if db_workflow:
#         raise HTTPException(status_code=400, detail="Workflow already registered")
#     return create(db=db, workflow=workflow)


@router.get("/", response_model=list[Workflow], operation_id="workflow_get_multi")
def read_workflows(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve worflows with their metadata.
    """
    workflows = WorkflowController.get_multi(db, skip=skip, limit=limit)
    return workflows


# @router.get("/{workflow_id}", response_model=WorkflowBase.Workflow)
# def read_workflow(workflow_id: str, db: Session = Depends(get_db)):
#     db_workflow = read_one(db, workflow_id=workflow_id)
#     if db_workflow is None:
#         raise HTTPException(status_code=404, detail="Workflow not found")
#     return db_workflow


# @router.put("/{workflow_id}", response_model=WorkflowBase.Workflow)
# def update_workflow(
#     workflow_id: str, workflow: WorkflowBase.Workflow, db: Session = Depends(get_db)
# ):
#     db_workflow = read_one(db, workflow_id=workflow_id)
#     if not db_workflow:
#         raise HTTPException(status_code=400, detail="Workflow does not exist")
#     return db_workflow


# @router.delete("/{workflow_id}")
# def delete_workflow(workflow_id: str, db: Session = Depends(get_db)):
#     db_workflow = read_one(db, workflow_id=workflow_id)
#     if db_workflow is None:
#         raise HTTPException(status_code=404, detail="Workflow not found")
#     return destroy(db=db, workflow=db_workflow)


# @router.get("/{workflow_id}/run", response_model=WorkflowBase.Run)
# def run_workflow(workflow_id: str, db: Session = Depends(get_db)):
#     db_run = createRun(db, workflow_id=workflow_id)

#     # db_workflow = read_one(db, workflow_id=workflow_id)
#     # db_run.next_steps = engine.Init(db_workflow.file, db_run.id)
#     db_run.next_steps = engine.Init("simple.json", db_run.id)
#     engine.CompleteStep(workflow_id, f"{db_run.id}.json")
#     return db_run


# @router.get("/{workflow_id}/task/{task_name}")
# def run_workflow(workflow_id: str, task_name: str, db: Session = Depends(get_db)):
#     # db_workflow = read_one(db, workflow_id=workflow_id)
#     # task = engine.GetTaskDetails(db_workflow.file, task_name)
#     try:
#         task = engine.GetTaskDetails("simple.json", task_name)
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     return task
