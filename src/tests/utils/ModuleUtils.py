from sqlalchemy.orm import Session
from uuid import UUID
from src.controllers.ModuleController import ModuleController
from src.models._all import ModuleModel
from src.schemas.ModuleSchema import ModuleCreate, ModuleUpdate
from ._base import (
    random_dict_obj,
    random_unique_string,
    random_lower_string,
)
from .ModuleCategoryUtils import seed_category


def create_random_module() -> tuple[str, dict]:
    name = random_unique_string()
    code = random_lower_string()
    task = random_lower_string()
    instructions = random_dict_obj()

    return name, code, task, instructions


def seed_module(db: Session) -> dict[str, dict, ModuleModel]:
    name, code, task, instructions = create_random_module()
    category = seed_category(db)

    module_in = ModuleCreate(
        category_id=category["obj"].id,
        name=name,
        code=code,
        task=task,
        instructions=instructions,
    )
    return {
        "category_id": category["obj"].id,
        "name": name,
        "code": code,
        "task": task,
        "instructions": instructions,
        "obj": ModuleController.create(db=db, obj_in=module_in),
    }


def update_seed_module(db: Session, module_id: UUID) -> dict[str, dict, ModuleModel]:
    name, _, task, instructions = create_random_module()

    module_update = ModuleUpdate(
        name=name,
        task=task,
        instructions=instructions,
    )
    return {
        "name": name,
        "task": task,
        "instructions": instructions,
        "obj": ModuleController.update(
            db=db, resource_id=module_id, resource_in=module_update
        ),
    }


def remove_module(db: Session, module_id: UUID) -> tuple[ModuleModel | None]:
    _ = ModuleController.destroy(
        db=db, resource_id=module_id, resource_in=ModuleUpdate()
    )
    try:
        module_validated = ModuleController.read(
            db=db, resource_id=module_id, criteria={"deleted_at": None}
        )
    except:
        module_validated = None

    return module_validated
