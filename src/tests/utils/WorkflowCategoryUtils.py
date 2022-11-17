from sqlalchemy.orm import Session
from uuid import UUID
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
    db: Session, category_id: UUID
) -> dict[str, dict, WorkflowCategoryModel]:
    name, code = create_random_category()

    category_update = WorkflowCategoryUpdate(name=name, code=code)
    return {
        "name": name,
        "code": code,
        "obj": WorkflowCategoryController.update(
            db=db, resource_id=category_id, resource_in=category_update
        ),
    }


def remove_category(
    db: Session, category_id: UUID
) -> tuple[WorkflowCategoryModel | None]:
    _ = WorkflowCategoryController.destroy(
        db=db, resource_id=category_id, resource_in=WorkflowCategoryUpdate()
    )
    try:
        category_validated = WorkflowCategoryController.read(
            db=db, resource_id=category_id, criteria={"deleted_at": None}
        )
    except:
        category_validated = None

    return category_validated
