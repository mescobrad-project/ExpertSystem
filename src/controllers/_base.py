from uuid import UUID
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy.orm import Session
from src.errors.ApiRequestException import (
    ConflictException,
    BadRequestException,
    InternalServerErrorException,
    NotFoundException,
)
from src.repositories._base import BaseCRUD, CreateSchemaType, UpdateSchemaType
from src.utils.pagination import paginate


class BaseController:
    def __init__(self, repository: BaseCRUD) -> None:
        self.repository = repository

    def create(self, db: Session, *, obj_in: CreateSchemaType):
        try:
            return self.repository.create(db=db, obj_in=obj_in)
        except IntegrityError as error:
            raise ConflictException(details=jsonable_encoder(error))
        except MultipleResultsFound as error:
            raise ConflictException(details=jsonable_encoder(error))
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

        if isinstance(resource_in, dict):
            resource_in["updated_at"] = datetime.now(tz=timezone.utc)
        else:
            resource_in.updated_at = datetime.now(tz=timezone.utc)

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

    def delete(self, db: Session, resource_id: UUID):
        return self.repository.remove(db=db, id=resource_id)
