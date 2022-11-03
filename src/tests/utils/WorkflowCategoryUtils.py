from sqlalchemy.orm import Session

from src.controllers.WorkflowCategoryController import WorkflowCategoryController
from src.models.WorkflowCategoryModel import WorkflowCategoryModel
from src.schemas.WorkflowCategorySchema import (
    WorkflowCategoryCreate,
    WorkflowCategoryUpdate,
)
from ._base import random_lower_string, random_unique_string, random_dict_obj


def create_random_category() -> tuple[str, dict]:
    name = random_unique_string()
    code = random_lower_string()

    return name, code


def seed_category(db: Session) -> dict[str, dict, WorkflowCategoryModel]:
    name, code = create_random_category()

    category_in = WorkflowCategoryCreate(name=name, code=code)
    return {
        "name": name,
        "code": code,
        "obj": WorkflowCategoryController.create(db=db, obj_in=category_in),
    }


def update_seed_category(
    db: Session, category: WorkflowCategoryModel
) -> dict[str, dict, WorkflowCategoryModel]:
    name, code = create_random_category()

    category_update = WorkflowCategoryUpdate(name=name, code=code)
    return {
        "name": name,
        "code": code,
        "obj": WorkflowCategoryController.update(
            db=db, db_obj=category, obj_in=category_update
        ),
    }


def remove_category(
    db: Session, category: WorkflowCategoryModel
) -> tuple[WorkflowCategoryModel | None]:
    _ = WorkflowCategoryController.remove(db=db, id=category.id)
    try:
        category_validated = WorkflowCategoryController.get(db=db, id=category.id)
    except:
        category_validated = None

    return category_validated
