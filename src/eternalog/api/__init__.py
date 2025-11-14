from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from eternalog.api.v1 import schemas as api_schemas  # pyright: ignore [reportMissingImports]

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

    @api.on_event("startup")
    async def on_startup():  # type: ignore[no-untyped-def]
        # Placeholder for future resource init (db pools, redis, etc.)
        pass

    @api.on_event("shutdown")
    async def on_shutdown():  # type: ignore[no-untyped-def]
        try:
            from eternalog.api import rate_limit  # pyright: ignore [reportMissingImports]

            rate_limit._buckets.clear()  # type: ignore[attr-defined]
            rate_limit._cache.clear()  # type: ignore[attr-defined]
        except Exception:
            pass

    @api.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):  # type: ignore[no-untyped-def]
        return JSONResponse(
            status_code=500,
            content=api_schemas.ErrorResponse(
                detail=str(exc), code="internal_error"
            ).model_dump(),
        )

    return api
