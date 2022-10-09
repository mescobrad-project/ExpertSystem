from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import workflow, run, home
from src.routers.datalake import objectstorage
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
    app.include_router(home.router)
    app.include_router(run.router)
    app.include_router(workflow.router)
    app.include_router(objectstorage.router)


def start_app():
    app = FastAPI(title=PROJECT_NAME)
    include_router(app)
    include_middlewares(app)
    create_tables()
    return app


main = start_app()
