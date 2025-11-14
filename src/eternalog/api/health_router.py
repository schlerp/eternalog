import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])  # pyright: ignore [reportArgumentType]


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
    # Future: DB / external checks
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}
