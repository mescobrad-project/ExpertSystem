from typing import Any, Generic, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from src.models._base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


def _parse_operations(key, prop, value):
    if key.endswith("__not"):
        return prop != value
    elif key.endswith("__gt"):
        return prop > value
    elif key.endswith("__gte"):
        return prop >= value
    elif key.endswith("__lt"):
        return prop < value
    elif key.endswith("__lte"):
        return prop <= value
    else:
        return prop == value


def _parse_criteria(model, criteria):
    filters = []
    for key, value in criteria.items():
        if type(value) is dict:
            model_ref = getattr(model, key)
            model_ref_class = value["model"]

            for m_key, m_value in value["criteria"].items():
                prop = getattr(model_ref_class, m_key.split("__")[0])
                filters.append(model_ref.has(_parse_operations(m_key, prop, m_value)))
        elif type(value) is list:
            prop = getattr(model, key)
            filters.append(prop.in_(value))
        else:
            prop = getattr(model, key.split("__")[0])
            filters.append(_parse_operations(key, prop, value))

    return filters


def _parse_order(model, order: str = None, direction: str = None):
    if order == None:
        order = "id"

    if direction == None:
        direction = "asc"

    if direction == "asc":
        return [asc(getattr(model, order))]
    if direction == "desc":
        return [desc(getattr(model, order))]


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get_one(
        self,
        db: Session,
        criteria={},
    ) -> ModelType | None:
        return (
            db.query(self.model)
            .filter(*_parse_criteria(self.model, criteria=criteria))
            .one()
        )

    def get(
        self,
        db: Session,
        id: Any,
        criteria={},
    ) -> ModelType | None:
        criteria["id"] = id

        return self.get_one(db, criteria)

    def count(self, db: Session, criteria={}) -> int:
        criteria["deleted_at"] = None
        return (
            db.query(self.model).filter(*_parse_criteria(self.model, criteria)).count()
        )

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        criteria={},
        order: str = None,
        direction: str = None,
    ) -> list[ModelType]:
        return (
            db.query(self.model)
            .filter(*_parse_criteria(self.model, criteria))
            .order_by(*_parse_order(self.model, order, direction))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
        fields_to_exclude: list | None = [],
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in, exclude=fields_to_exclude)
        if fields_to_exclude:
            for field in fields_to_exclude:
                obj_in_data[field] = getattr(obj_in, field)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
        fields_to_exclude: list | None = [],
    ) -> ModelType:
        """
        fields_to_exclude is a list for fields to not be parsed as JSON. This is an error
        that is raised because of some models that need custom Objects (e.g. SQLAlchemy model)
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                if field not in fields_to_exclude:
                    setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_multi(
        self,
        db: Session,
        *,
        obj_in: UpdateSchemaType | dict[str, Any],
        criteria={},
    ) -> int:
        """
        Update multiple rows based on the given criteria.
        """
        # Parse the update data
        if isinstance(obj_in, dict):
            values = obj_in
        else:
            values = obj_in.dict(exclude_unset=True)

        # Perform the bulk update
        query = db.query(self.model).filter(*_parse_criteria(self.model, criteria))
        result = query.update(values, synchronize_session=False)

        db.commit()
        return result

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
