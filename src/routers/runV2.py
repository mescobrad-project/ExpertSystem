from typing import Any
from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.controllers.RunController import RunController
from src.dependencies.authentication import validate_user
from src.dependencies.workspace import validate_workspace
from src.services.NewRunService import (
    createRun,
    get_all_runs,
    get_data_from_querybuilder,
    get_trino_tables,
    query_trino_table,
    get_variables,
    get_trino_schema,
    getActionInputForQueryBuilder,
    get_buckets_from_minio,
    saveAction,
    get_run,
    getAction,
    next_step,
    get_table_data,
    delete_run,
)
from src.schemas.RequestBodySchema import (
    TaskMetadataBodyParameter,
    CallActivityParams,
)
from src.schemas.NewRunSchema import Run, RunAction, RunActionUpdateFromQB

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"message": "Not found"}},
    # dependencies=[Depends(validate_user)],
)


@router.post("/workflow/{workflow_id}", response_model=Run)
def run_workflow(
    *,
    db: Session = Depends(get_db),
    request: Request,
    workflow_id: UUID,
    data: dict = {},
):
    """
    Initiate a workflow process
    """
    return RunController.initialize(
        db=db,
        ws_id=request.headers.get("x-es-wsid"),
        workflow_id=workflow_id,
        name=data.get("name", ""),
        settings=data.get("settings", {}),
    )


@router.get("/buckets", response_model=Any)
def get_buckets(*, request: Request) -> Any:
    """
    Get all buckets
    """

    return get_buckets_from_minio(request.headers.get("x-jwt-token"))


@router.get("/tables", response_model=Any)
def getTables(*, request: Request) -> Any:
    """
    Get all tables
    """

    return get_trino_tables(request.headers.get("x-jwt-token"))


@router.get("/query", response_model=Any)
def runQuery(
    *,
    table: str = None,
    vname: str | None,
    vvalue: str | None,
    request: Request,
) -> Any:
    """
    Run query
    """

    return query_trino_table(table, vname, vvalue, request.headers.get("x-jwt-token"))


@router.get("/table_data", response_model=Any)
def get_data_from_trino_table(
    *, table: str, source: str, request: Request, vname: str = "", vvalue: str = ""
) -> Any:
    return get_table_data(
        table, source, request.headers.get("x-jwt-token"), vname, vvalue
    )


@router.get("/files", response_model=Any)
def getFiles(*, table: str, request: Request) -> Any:
    """
    Get all files
    """

    return query_trino_table(table, "", "", request.headers.get("x-jwt-token"))


@router.get("/variable_names", response_model=Any)
def getVariableNames(*, table: str, request: Request) -> Any:
    """
    Get variable names
    """

    return get_variables(table, request.headers.get("x-jwt-token"))


@router.get("/schema", response_model=Any)
def getSchema(*, request: Request) -> Any:
    """
    Get schema
    """

    return get_trino_schema(request.headers.get("x-jwt-token"))


@router.post("", response_model=Any)
def create_run(
    *,
    db: Session = Depends(get_db),
    data: Run,
    request: Request,
):
    """
    Run a task
    """
    return createRun(db, data, request.headers.get("x-es-wsid"))


@router.post("/{run_id}/action", response_model=Any)
def create_action(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    data: RunAction,
):
    """
    Save action
    """
    return saveAction(db, data)


@router.get("/{run_id}/step/{action_id}/ping", response_model=Any)
def get_action(
    *, db: Session = Depends(get_db), run_id: str, action_id: str, request: Request
):
    """
    Get action
    """
    return getActionInputForQueryBuilder(
        db, action_id, run_id, request.headers.get("x-jwt-token")
    )


@router.patch("/{run_id}/step/{step_id}/task/script/complete", response_model=Any)
def value_from_qb(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    step_id: UUID,
    data: dict,
) -> Any:
    """
    Get value from query builder
    """
    return get_data_from_querybuilder(db, run_id, step_id, data)


@router.put("/{run_id}/next", response_model=Any)
def nextStep(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
):
    """
    Get next step
    """
    return next_step(db, run_id)


@router.put("/{run_id}/complete", response_model=Any)
def complete_run(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
):
    """
    Complete run
    """
    return RunController.complete_run(db, run_id)


@router.get("", response_model=Any)
def get_runs(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    workflow_id: UUID | None = None,
    request: Request,
):
    """
    Get runs
    """
    return get_all_runs(db, request.headers.get("x-es-wsid"), workflow_id, skip, limit)


@router.get("/{run_id}", response_model=Any)
def get_single_run(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    request: Request,
):
    """
    Get run
    """
    return get_run(db, request.headers.get("x-es-wsid"), run_id)


@router.get("/{run_id}/{action_id}", response_model=Any)
def get_action(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
    action_id: UUID,
):
    """
    Get action
    """
    return getAction(db, action_id)


@router.delete("/{run_id}", response_model=Any)
def delete_run_route(
    *,
    db: Session = Depends(get_db),
    run_id: UUID,
):
    """
    Delete run
    """
    return delete_run(db, run_id)
