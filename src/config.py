from os import getenv
from pathlib import Path

WORKDIR = Path(__file__).parent.resolve()

APP_HOSTS = (getenv("APP_HOSTS", "http://localhost")).split(",")
APP_ROOT = getenv("APP_ROOT", "/")

AI_API_BASE_URL = getenv("ARTIFICIAL_INTELLIGENCE_API_BASE_URL", "http://localhost")
QB_API_BASE_URL = getenv("QUERY_BUILDER_API_BASE_URL", "http://localhost")
DA_API_BASE_URL = getenv("DATA_ANALYTICS_API_BASE_URL", "http://localhost")

CORS_ORIGINS = (getenv("CORS_ORIGINS", "http://localhost,localhost")).split(",")
CORS_CREDENTIALS = getenv("CORS_CREDENTIALS", True)
CORS_METHODS = (getenv("CORS_METHODS", "*")).split(",")
CORS_HEADERS = (getenv("CORS_HEADERS", "*")).split(",")

DB_CONNECTION = getenv("DB_CONNECTION", "postgresql")
DB_SCHEMA = getenv("DB_SCHEMA", "public")
DB_HOST = getenv("DB_HOST", "localhost")
DB_PORT = getenv("DB_PORT", 5432)
DB_DATABASE = getenv("DB_DATABASE", "test_db")
DB_USERNAME = getenv("DB_USERNAME", "test_user")
DB_PASSWORD = getenv("DB_PASSWORD", "")

S3_ENDPOINT = getenv("S3_ENDPOINT", "localhost")
S3_ACCESS_KEY_ID = getenv("S3_ACCESS_KEY_ID", "access_key")
S3_SECRET_ACCESS_KEY = getenv("S3_SECRET_ACCESS_KEY", "secret_key")

SQLALCHEMY_DATABASE_URL = (
    f"{DB_CONNECTION}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
)

PROJECT_NAME = getenv("APP_NAME", "test_app")

OAUTH_HOST = getenv("OAUTH_HOST", "https://sso.example.com/auth/")
OAUTH_TOKEN_URL = getenv("OAUTH_TOKEN_URL", "https://sso.example.com/token/")
OAUTH_CLIENT_ID = getenv("OAUTH_CLIENT_ID", "client-id")
OAUTH_CLIENT_SECRET = getenv("OAUTH_CLIENT_SECRET", "client-secret")
OAUTH_REALM = getenv("OAUTH_REALM", "realm")
OAUTH_CALLBACK_URL = getenv("OAUTH_CALLBACK_URL", "https://app.example.com/")
OAUTH_SIGN_OUT_URL = getenv(
    "OAUTH_SIGN_OUT_URL", "https://app.example.com/auth/logout/"
)
OAUTH_LOGIN_SCOPE = getenv("OAUTH_LOGIN_SCOPE", "openid,profile")

ENCRYPTION_KEY = getenv("ENCRYPTION_KEY", "")
