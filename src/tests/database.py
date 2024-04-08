from fastapi import Request
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .config import SQLALCHEMY_DATABASE_URL
from src.models._all import Base
from src.config import DB_SCHEMA

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
with engine.connect() as conn:
    conn.execute(text(f"ATTACH ':memory:' AS {DB_SCHEMA};"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(engine)
