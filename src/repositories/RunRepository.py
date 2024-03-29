from uuid import UUID
from ._base import BaseCRUD, Session, ModelType
from src.models._all import RunModel
from src.schemas.RunSchema import RunCreate, RunUpdate


class _RunRepository(BaseCRUD[RunModel, RunCreate, RunUpdate]):
    def initialize(self, db: Session, *, workflow_id: UUID) -> ModelType:
        run_in = RunCreate(
            workflow_id=workflow_id,
            state={"completed": False, "success": False, "step": 0},
            steps=[],
            queue=[],
        )

        return self.create(db=db, obj_in=run_in)


RunRepository = _RunRepository(RunModel)
