from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from .database import SessionLocal as SessionTesting, create_tables, drop_tables, engine
from src.routers import workflow


def start_application():
    main = FastAPI()
    main.include_router(workflow.router)
    return main


@pytest.fixture(scope="session")
def db() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    create_tables()
    yield session  # use the session in tests.
    session.close()
    transaction.rollback()
    connection.close()
    drop_tables()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(start_application()) as c:
        yield c
