from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy.orm import Session
from uuid import UUID
from src.errors.ApiRequestException import (
    ConflictException,
    BadRequestException,
    InternalServerErrorException,
)
from src.repositories.VariableRepository import VariableRepository
from src.repositories.FeatureRepository import FeatureRepository
from src.schemas.FeatureSchema import FeatureUpdate, FeatureCreate
from ._base import BaseController


class _FeatureController(BaseController):
    def create(self, db: Session, *, obj_in: FeatureCreate):
        try:
            fields_to_exclude = []
            if obj_in.variables:
                obj_in.variables = VariableRepository.get_multi(
                    db=db, criteria={"id": obj_in.variables}
                )
                fields_to_exclude = ["variables"]

            return self.repository.create(
                db=db, obj_in=obj_in, fields_to_exclude=fields_to_exclude
            )
        except IntegrityError as error:
            raise ConflictException(details=jsonable_encoder(error))
        except MultipleResultsFound as error:
            raise ConflictException(details=jsonable_encoder(error))
        except Exception as error:
            raise BadRequestException(
                message="Provided input is wrong", details=jsonable_encoder(error)
            )

    def update(
        self,
        db: Session,
        resource_id: UUID,
        resource_in: FeatureUpdate,
        criteria={"deleted_at": None},
    ):
        resource = self.read(db=db, resource_id=resource_id, criteria=criteria)

        try:
            if resource_in.variables:
                resource.variables = VariableRepository.get_multi(
                    db=db, criteria={"id": resource_in.variables}
                )

                return self.repository.update(
                    db=db,
                    db_obj=resource,
                    obj_in=resource_in,
                    fields_to_exclude=["variables"],
                )
            else:
                resource.variables = []

                return self.repository.update(
                    db=db, db_obj=resource, obj_in=resource_in
                )
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))


FeatureController = _FeatureController(FeatureRepository)
