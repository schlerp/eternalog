from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from eternalog.api.v1 import schemas as api_schemas  # pyright: ignore [reportMissingImports]

from eternalog.api.v1 import v1_router
from eternalog.api.health_router import router as health_router  # pyright: ignore [reportMissingImports]


from contextlib import asynccontextmanager


def create_api() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):  # type: ignore[no-untyped-def]
        # Startup
        yield
        # Shutdown cleanup
        try:
            from eternalog.api import rate_limit  # pyright: ignore [reportMissingImports]

            rate_limit._buckets.clear()  # type: ignore[attr-defined]
            rate_limit._cache.clear()  # type: ignore[attr-defined]
        except Exception:
            pass

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
        lifespan=lifespan,
    )
    api.include_router(health_router)
    api.include_router(v1_router)

    @api.middleware("http")
    async def request_id_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        import uuid

        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response

    @api.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):  # type: ignore[no-untyped-def]
        return JSONResponse(
            status_code=500,
            content=api_schemas.ErrorResponse(
                detail=str(exc), code="internal_error"
            ).model_dump(),
        )

    return api
