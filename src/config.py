from os import getenv
from pathlib import Path

WORKDIR = Path(__file__).parent.resolve()

CORS_ORIGINS = (getenv("CORS_ORIGINS", "http://localhost,localhost")).split(",")
CORS_CREDENTIALS = getenv("CORS_CREDENTIALS", True)
CORS_METHODS = (getenv("CORS_METHODS", "*")).split(",")
CORS_HEADERS = (getenv("CORS_HEADERS", "*")).split(",")
