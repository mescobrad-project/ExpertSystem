from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.routers import (
    workflow,
    run,
    feature,
    file,
    home,
    module_category,
    module,
    variable,
    workflow_category,
    oauth,
    auth,
    workspace,
    workflowV2,
    runV2,
)
from src.routers.datalake import objectstorage, datastorage
from src.config import (
    CORS_ORIGINS,
    CORS_CREDENTIALS,
    CORS_METHODS,
    CORS_HEADERS,
    PROJECT_NAME,
)
from src.database import create_tables


def include_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=CORS_CREDENTIALS,
        allow_methods=CORS_METHODS,
        allow_headers=CORS_HEADERS,
    )


def include_router(app):
    app.include_router(feature.router)
    app.include_router(file.router)
    app.include_router(home.router)
    app.include_router(oauth.router)
    app.include_router(run.router)
    app.include_router(variable.router) 
    app.include_router(workflow_category.router)
    app.include_router(workflow.router)
    app.include_router(workspace.router)
    app.include_router(module_category.router)
    app.include_router(module.router)
    app.include_router(objectstorage.router)
    app.include_router(datastorage.router)
    app.include_router(workflowV2.router)
    app.include_router(runV2.router)
    app.include_router(auth.router)


def start_app():
    app = FastAPI(
        title=PROJECT_NAME,
    )
    include_router(app)
    include_middlewares(app)
    create_tables()
    return app


main = start_app()


@main.exception_handler(StarletteHTTPException)
async def http_exception_handler(_: Request, exc: StarletteHTTPException):
    if type(exc.detail) == str:
        return JSONResponse(
            content={
                "details": exc.detail,
            },
            status_code=exc.status_code,
        )

    return JSONResponse(
        content={
            "message": exc.detail.get("message"),
            "details": exc.detail.get("details"),
            "id": exc.detail.get("id"),
        },
        status_code=exc.status_code,
    )


@main.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        content=jsonable_encoder({"message": str(exc), "details": exc.errors()}),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
