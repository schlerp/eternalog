from fastapi import FastAPI

from eternalog.api.v1 import v1_router


def create_api() -> FastAPI:
    api = FastAPI(
        title="Eternalog",
        description="An immutable log storage/versioning service.",
        version="0.1.0",
    )
    api.include_router(v1_router)
    return api
