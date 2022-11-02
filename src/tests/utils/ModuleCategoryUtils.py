from sqlalchemy.orm import Session

from src.controllers.ModuleCategoryController import ModuleCategoryController
from src.models.ModuleCategoryModel import ModuleCategoryModel
from src.schemas.ModuleCategorySchema import ModuleCategoryCreate, ModuleCategoryUpdate
from ._base import random_lower_string, random_unique_string, random_dict_obj


def create_random_category() -> tuple[str, dict]:
    name = random_unique_string()
    code = random_lower_string()

    return name, code


def seed_category(db: Session) -> dict[str, dict, ModuleCategoryModel]:
    name, code = create_random_category()

    category_in = ModuleCategoryCreate(name=name, code=code)
    return {
        "name": name,
        "code": code,
        "obj": ModuleCategoryController.create(db=db, obj_in=category_in),
    }


def update_seed_category(
    db: Session, category: ModuleCategoryModel
) -> dict[str, dict, ModuleCategoryModel]:
    name, code = create_random_category()

    category_update = ModuleCategoryUpdate(name=name, code=code)
    return {
        "name": name,
        "code": code,
        "obj": ModuleCategoryController.update(
            db=db, db_obj=category, obj_in=category_update
        ),
    }


def remove_category(
    db: Session, category: ModuleCategoryModel
) -> tuple[ModuleCategoryModel | None]:
    _ = ModuleCategoryController.remove(db=db, id=category.id)
    try:
        category_validated = ModuleCategoryController.get(db=db, id=category.id)
    except:
        category_validated = None

    return category_validated
