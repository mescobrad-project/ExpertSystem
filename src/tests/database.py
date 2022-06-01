from fastapi import Request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import SQLALCHEMY_DATABASE_URL
from src.models._all import Base

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db(request: Request):
    return request.state.db


def create_tables():
    Base.metadata.create_all(bind=engine)


def drop_tables():
    Base.metadata.drop_all(engine)
