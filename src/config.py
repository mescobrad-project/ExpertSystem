from os import getenv
from pathlib import Path

WORKDIR = Path(__file__).parent.resolve()

CORS_ORIGINS = (getenv("CORS_ORIGINS", "http://localhost,localhost")).split(",")
CORS_CREDENTIALS = getenv("CORS_CREDENTIALS", True)
CORS_METHODS = (getenv("CORS_METHODS", "*")).split(",")
CORS_HEADERS = (getenv("CORS_HEADERS", "*")).split(",")

DB_CONNECTION = getenv("DB_CONNECTION", "postgresql")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", 5432)
DB_DATABASE = getenv("DB_DATABASE", "test_db")
DB_USERNAME = getenv("DB_USERNAME", "test_user")
DB_PASSWORD = getenv("DB_PASSWORD", "")

SQLALCHEMY_DATABASE_URL = (
    f"{DB_CONNECTION}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

PROJECT_NAME = getenv("APP_NAME", "test_app")
