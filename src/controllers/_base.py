from typing import Any, Generic, Type, TypeVar
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import asc, desc

#
from uuid import UUID
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src.errors.ApiRequestException import (
    ConflictException,
    BadRequestException,
    InternalServerErrorException,
    NotFoundException,
)
from src.repositories._base import BaseCRUD
from src.utils.pagination import paginate


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


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(
        self,
        db: Session,
        id: Any,
        criteria={},
    ) -> ModelType | None:
        criteria["id"] = id

        return (
            db.query(self.model)
            .filter(*_parse_criteria(self.model, criteria=criteria))
            .first()
        )

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

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
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
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


class BaseController:
    def __init__(self, repository: BaseCRUD) -> None:
        self.repository = repository

    def create(self, db: Session, *, obj_in: CreateSchemaType):
        try:
            return self.repository.create(db=db, obj_in=obj_in)
        except IntegrityError:
            raise ConflictException(details=f"Resource already exists")
        except Exception as error:
            raise BadRequestException(
                message="Provided input is wrong", details=jsonable_encoder(error)
            )

    def read_multi(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        order: str = None,
        direction: str = None,
        criteria: dict = {},
    ):
        try:
            if skip < 0:
                skip = 0

            data = self.repository.get_multi(
                db,
                skip=skip,
                limit=limit,
                criteria=criteria,
                order=order,
                direction=direction,
            )
            count_all = self.repository.count(db, criteria=criteria)

            paging = paginate(count_all, skip, limit)
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))

        return {
            "data": data,
            "paging": paging,
            "count": count_all,
        }

    def read(self, db: Session, resource_id: UUID, criteria: dict = {}):
        data = self.repository.get(db=db, id=resource_id, criteria=criteria)

        if not data:
            raise NotFoundException(details="Resource not found")

        return data

    def update(
        self,
        db: Session,
        resource_id: UUID,
        resource_in: UpdateSchemaType,
        criteria={"deleted_at": None},
    ):
        resource = self.read(db=db, resource_id=resource_id, criteria=criteria)

        try:
            return self.repository.update(db=db, db_obj=resource, obj_in=resource_in)
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))

    def destroy(self, db: Session, resource_id: UUID, resource_in: UpdateSchemaType):
        resource_in.deleted_at = datetime.now(tz=timezone.utc)

        return self.update(db=db, resource_id=resource_id, resource_in=resource_in)

    def revert(self, db: Session, resource_id: UUID, resource_in: UpdateSchemaType):
        resource_in.deleted_at = None

        return self.update(
            db=db,
            resource_id=resource_id,
            resource_in=resource_in,
            criteria={"deleted_at__not": None},
        )
