from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import workflow
from src.config import CORS_ORIGINS, CORS_CREDENTIALS, CORS_METHODS, CORS_HEADERS

main = FastAPI()

main.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_CREDENTIALS,
    allow_methods=CORS_METHODS,
    allow_headers=CORS_HEADERS,
)

main.include_router(workflow.router)
