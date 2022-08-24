from sqlalchemy.orm import Session

from src.controllers.RunController import RunController
from src.models.RunModel import RunModel
from src.schemas.RunSchema import RunCreate, RunUpdate
from ._base import random_dict_obj, random_listofdict_obj
from .WorkflowUtils import seed_workflow


def create_random_run() -> tuple[str, dict]:
    state = random_dict_obj()
    steps = random_listofdict_obj()
    queue = random_listofdict_obj()

    return state, steps, queue


def seed_run(db: Session) -> dict[str, dict, RunModel]:
    state, steps, queue = create_random_run()
    workflow = seed_workflow(db)

    run_in = RunCreate(
        workflow_id=workflow["obj"].id, state=state, steps=steps, queue=queue
    )
    return {
        "workflow_id": workflow["obj"].id,
        "state": state,
        "steps": steps,
        "queue": queue,
        "obj": RunController.create(db=db, obj_in=run_in),
    }


def update_seed_run(db: Session, run: RunModel) -> dict[str, dict, RunModel]:
    state, steps, queue = create_random_run()

    run_update = RunUpdate(state=state, steps=steps, queue=queue)
    return {
        "state": state,
        "steps": steps,
        "queue": queue,
        "obj": RunController.update(db=db, db_obj=run, obj_in=run_update),
    }


def remove_run(db: Session, run: RunModel) -> tuple[RunModel | None]:
    _ = RunController.remove(db=db, id=run.id)
    try:
        run_validated = RunController.get(db=db, id=run.id)
    except:
        run_validated = None

    return run_validated