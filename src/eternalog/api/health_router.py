import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])  # pyright: ignore [reportArgumentType]


@router.get("/live")
def live() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
    # Future: DB / external checks
    return {"status": "ok", "time": datetime.datetime.now(datetime.UTC).isoformat()}


from fastapi import Request


@router.get("/info")
def info(request: Request) -> dict[str, str]:  # type: ignore[no-untyped-def]
    commit = getattr(request.app.state, "commit", "unknown")  # type: ignore[attr-defined]
    start_time = getattr(request.app.state, "start_time", None)  # type: ignore[attr-defined]
    return {
        "status": "ok",
        "commit": commit,
        "start_time": start_time.isoformat() if start_time else "unknown",
    }
