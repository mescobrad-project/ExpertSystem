from uuid import UUID
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from src.errors.ApiRequestException import InternalServerErrorException
from src.repositories._base import ModelType
from src.repositories.RunRepository import RunRepository
from src.schemas.RunSchema import RunCreate, RunUpdate
from ._base import BaseController
from .WorkflowController import WorkflowController
from .WorkflowEngineController import WorkflowEngineController


class _RunController(BaseController):
    def initialize(self, db: Session, *, workflow_id: UUID) -> ModelType:
        workflow = WorkflowController.read(db=db, resource_id=workflow_id)

        run = super().create(
            db=db,
            obj_in=RunCreate(
                workflow_id=workflow_id,
                state={"completed": False, "success": False, "step": 0},
                steps=[],
                queue=[],
            ),
        )

        try:
            state, steps, queue = WorkflowEngineController.initialize(workflow.tasks)
        except Exception as error:
            raise InternalServerErrorException(details=jsonable_encoder(error))

        return super().update(
            db=db,
            resource_id=run.id,
            resource_in=RunUpdate(state=state, steps=steps, queue=queue),
        )

    def update_name(self, db: Session, resource_id: UUID, name: str):
        return super().update(db, resource_id, RunUpdate(name=name))

    def _run_execution_wrapper(self, func: any, db: Session, run_id: UUID, *args):
        run = super().read(db=db, resource_id=run_id, criteria={"deleted_at": None})

        run_in = jsonable_encoder(run)
        workflow = jsonable_encoder(run.workflow)
        try:
            error_if_existed = ""
            try:
                response = func(
                    workflow,
                    run_in,
                    *args,
                )
            except Exception as error:
                error_if_existed = str(error)
                response = WorkflowEngineController.task_revert(
                    workflow, run_in, step_id=str(args[0])
                )
                pass
            finally:
                super().update(db=db, resource_id=run_id, resource_in=run_in)
                pass

            if error_if_existed != "":
                raise Exception(error_if_existed)

            return response
        except Exception as error:
            raise InternalServerErrorException(details=str(error))

    def get_next_task(self, db: Session, run_id: UUID):
        return self._run_execution_wrapper(
            WorkflowEngineController.get_waiting_steps, db, run_id
        )

    def get_dataobjects_from_stored_data(self, db: Session, run_id: UUID):
        run = super().read(db=db, resource_id=run_id, criteria={"deleted_at": None})

        try:
            return WorkflowEngineController.get_dataobject_refs(run)
        except Exception as error:
            raise InternalServerErrorException(details=str(error))

    def run_specific_task(self, db: Session, run_id: UUID, step_id: UUID):
        return self._run_execution_wrapper(
            WorkflowEngineController.run_pending_step,
            db,
            run_id,
            step_id,
        )

    def select_next_task(
        self, db: Session, run_id: UUID, step_id: UUID, next_step_id: UUID
    ):
        return self._run_execution_wrapper(
            WorkflowEngineController.gateway_exclusive_choice,
            db,
            run_id,
            step_id,
            next_step_id,
        )

    def init_parallel_gateway(
        self, db: Session, run_id: UUID, step_id: UUID, next_step_id: UUID
    ):
        return self._run_execution_wrapper(
            WorkflowEngineController.gateway_parallel_choice,
            db,
            run_id,
            step_id,
            next_step_id,
        )

    def exec_script_task(self, db: Session, run_id: UUID, step_id: UUID, data: any):
        return self._run_execution_wrapper(
            WorkflowEngineController.task_exec,
            db,
            run_id,
            step_id,
            data,
        )

    def send_task(self, db: Session, run_id: UUID, step_id: UUID, data: any):
        return self._run_execution_wrapper(
            WorkflowEngineController.task_send,
            db,
            run_id,
            step_id,
            data,
        )

    def receive_task(self, db: Session, run_id: UUID, step_id: UUID, data: any):
        return self._run_execution_wrapper(
            WorkflowEngineController.task_receive,
            db,
            run_id,
            step_id,
            data,
        )

    def complete_task(self, db: Session, run_id: UUID, step_id: UUID, data: any):
        return self._run_execution_wrapper(
            WorkflowEngineController.task_complete,
            db,
            run_id,
            step_id,
            data,
        )

    def complete_script_task(self, db: Session, run_id: UUID, step_id: UUID, data: any):
        return self._run_execution_wrapper(
            WorkflowEngineController.task_script_complete,
            db,
            run_id,
            step_id,
            data,
        )

    def exec_event_task_actions(self, db: Session, run_id: UUID, step_id: UUID):
        return self._run_execution_wrapper(
            WorkflowEngineController.event_actions,
            db,
            run_id,
            step_id,
        )

    def ping_task_status(self, db: Session, run_id: UUID, step_id: UUID):
        return self._run_execution_wrapper(
            WorkflowEngineController.ping_step_status,
            db,
            run_id,
            step_id,
        )


RunController = _RunController(RunRepository)
