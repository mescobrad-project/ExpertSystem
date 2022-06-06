from sqlalchemy.orm import Session

from src.controllers.RunController import RunController
from src.tests.utils._base import check_if_dicts_match, check_if_listofdicts_match
from src.tests.utils.RunUtils import (
    seed_run,
    remove_run,
    update_seed_run,
)


def test_create_run(db: Session) -> None:
    run = seed_run(db)

    assert run["obj"].workflow_id == run["workflow_id"]
    assert check_if_dicts_match(run["obj"].state, run["state"])
    assert check_if_listofdicts_match(run["obj"].steps, run["steps"])
    assert check_if_listofdicts_match(run["obj"].queue, run["queue"])


def test_get_run(db: Session) -> None:
    run = seed_run(db)

    stored = RunController.get(db=db, id=run["obj"].id)
    assert stored
    assert run["obj"].workflow_id == stored.workflow_id
    assert check_if_dicts_match(run["obj"].state, stored.state)
    assert check_if_listofdicts_match(run["obj"].steps, stored.steps)
    assert check_if_listofdicts_match(run["obj"].queue, stored.queue)


def test_update_run(db: Session) -> None:
    run1 = seed_run(db)
    run2 = update_seed_run(db, run1["obj"])

    assert check_if_dicts_match(run2["obj"].state, run2["state"])
    assert check_if_listofdicts_match(run2["obj"].steps, run2["steps"])
    assert check_if_listofdicts_match(run2["obj"].queue, run2["queue"])


def test_delete_run(db: Session) -> None:
    run = seed_run(db)
    run_validate = remove_run(db, run["obj"])

    assert run_validate is None
