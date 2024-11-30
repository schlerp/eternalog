import pydantic
from fastapi import APIRouter

ROUTER_TAGS: list[str] = ["Test", "v1"]
ROUTER_PATH = "/test"

router = APIRouter(
    prefix=ROUTER_PATH,
    tags=ROUTER_TAGS,
    responses={404: {"description": "Not found"}},
)


class TestResponse(pydantic.BaseModel):
    message: str


@router.get("/echo/{message}")
def echo(message: str) -> TestResponse:
    return TestResponse(message=message)
