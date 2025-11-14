from fastapi import FastAPI

from eternalog.api.v1 import v1_router
from eternalog.api.health_router import router as health_router  # pyright: ignore [reportMissingImports]


def create_api() -> FastAPI:
    api = FastAPI(
        title="Eternalog",
        description="An immutable log storage/versioning service.",
        version="0.1.0",
        openapi_tags=[
            {
                "name": "log_entries",
                "description": "Operations on stored log entries with pagination, filtering, and sorting.",
            },
            {"name": "health", "description": "Health and readiness checks."},
        ],
    )
    api.include_router(health_router)
    api.include_router(v1_router)
    return api
