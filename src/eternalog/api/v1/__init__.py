from fastapi import APIRouter

from eternalog.api.v1 import test_router

v1_router = APIRouter(
    prefix="/api/v1",
    tags=["v1"],
)
v1_router.include_router(test_router.router, tags=test_router.ROUTER_TAGS)
