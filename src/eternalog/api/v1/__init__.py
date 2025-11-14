from fastapi import APIRouter

from eternalog.api.v1 import test_router
from eternalog.api.v1 import log_entry_router

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)
v1_router.include_router(test_router.router, tags=test_router.ROUTER_TAGS)  # pyright: ignore [reportArgumentType]
v1_router.include_router(log_entry_router.router, tags=log_entry_router.ROUTER_TAGS)  # pyright: ignore [reportArgumentType]
