from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from uuid import UUID
from src.errors.ApiRequestException import (
    ConflictException,
    BadRequestException,
    InternalServerErrorException,
)
from src.repositories.FeatureRepository import FeatureRepository
from src.repositories.VariableRepository import VariableRepository
from src.schemas.VariableSchema import VariableUpdate, VariableCreate
from ._base import BaseController


class _VariableController(BaseController):
    def create(self, db: Session, *, obj_in: VariableCreate):
        try:
            fields_to_exclude = []
            if obj_in.features:
                obj_in.features = VariableRepository.get_multi(
                    db=db, criteria={"id": obj_in.features}
                )
                fields_to_exclude = ["features"]

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
        resource_in: VariableUpdate,
        criteria={"deleted_at": None},
    ):
        resource = self.read(db=db, resource_id=resource_id, criteria=criteria)

        if resource_in.features:
            resource.features = FeatureRepository.get_multi(
                db=db, criteria={"id": resource_in.features}
            )
        else:
            resource.features = []

        try:
            return self.repository.update(
                db=db,
                db_obj=resource,
                obj_in=resource_in,
                fields_to_exclude=["features"],
            )
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))


VariableController = _VariableController(VariableRepository)
