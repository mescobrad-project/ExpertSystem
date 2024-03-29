from sqlalchemy.orm import Session

from src.controllers.ModuleCategoryController import ModuleCategoryController
from src.tests.utils._base import check_if_dicts_match
from src.tests.utils.ModuleCategoryUtils import (
    seed_category,
    remove_category,
    update_seed_category,
)


def test_create_category(db: Session) -> None:
    category = seed_category(db)

    assert category["obj"].name == category["name"]
    assert category["obj"].code == category["code"]


def test_get_category(db: Session) -> None:
    category = seed_category(db)

    stored = ModuleCategoryController.read(
        db=db, resource_id=category["obj"].id, criteria={"deleted_at": None}
    )
    assert stored
    assert category["obj"].name == stored.name
    assert category["obj"].code == stored.code


def test_update_category(db: Session) -> None:
    category1 = seed_category(db)
    category2 = update_seed_category(db, category1["obj"].id)

    assert category2["obj"].name == category2["name"]
    assert category2["obj"].code == category2["code"]


def test_delete_category(db: Session) -> None:
    category = seed_category(db)
    category_validate = remove_category(db, category["obj"].id)

    assert category_validate is None
