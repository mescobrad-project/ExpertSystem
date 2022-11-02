from sqlalchemy.orm import Session

from src.controllers.ModuleController import ModuleController
from src.tests.utils._base import check_if_dicts_match, check_if_listofdicts_match
from src.tests.utils.ModuleUtils import (
    seed_module,
    remove_module,
    update_seed_module,
)


def test_create_module(db: Session) -> None:
    module = seed_module(db)

    assert module["obj"].category_id == module["category_id"]
    assert module["obj"].name == module["name"]
    assert module["obj"].code == module["code"]
    assert module["obj"].task == module["task"]
    assert check_if_dicts_match(module["obj"].instructions, module["instructions"])


def test_get_module(db: Session) -> None:
    module = seed_module(db)

    stored = ModuleController.get(db=db, id=module["obj"].id)
    assert stored
    assert module["obj"].category_id == stored.category_id
    assert module["obj"].name == stored.name
    assert module["obj"].code == stored.code
    assert module["obj"].task == stored.task
    assert check_if_dicts_match(module["obj"].instructions, stored.instructions)


def test_update_module(db: Session) -> None:
    module1 = seed_module(db)
    module2 = update_seed_module(db, module1["obj"])

    assert module2["obj"].name == module2["name"]
    assert module2["obj"].task == module2["task"]
    assert check_if_dicts_match(module2["obj"].instructions, module2["instructions"])


def test_delete_module(db: Session) -> None:
    module = seed_module(db)
    module_validate = remove_module(db, module["obj"])

    assert module_validate is None
