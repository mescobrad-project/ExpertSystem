from uuid import UUID
from sqlalchemy.orm import Session
from src.repositories._base import ModelType
from src.repositories.RunRepository import RunRepository
from src.schemas.RunSchema import RunCreate
from ._base import BaseController


class _RunController(BaseController):
    def initialize(self, db: Session, *, workflow_id: UUID) -> ModelType:
        run_in = RunCreate(
            workflow_id=workflow_id,
            state={"completed": False, "success": False, "step": 0},
            steps=[],
            queue=[],
        )

        return self.create(db=db, obj_in=run_in)


RunController = _RunController(RunRepository)
