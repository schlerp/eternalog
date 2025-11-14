import datetime
import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from sqlalchemy.orm import Session

from eternalog.api.v1 import schemas as api_schemas
from eternalog.data import connection
from eternalog.data import core as data_core
from eternalog.api.auth import api_key_auth  # pyright: ignore [reportMissingImports]

ROUTER_TAGS: list[str] = ["log_entries"]
ROUTER_PATH = ""

router = APIRouter(
    prefix=ROUTER_PATH,
    tags=ROUTER_TAGS,  # pyright: ignore [reportArgumentType]
    responses={404: {"description": "Not found"}},
)


from collections.abc import Generator


def get_db() -> Generator[Session, None, None]:  # dependency
    with connection.get_db_session() as db:
        yield db


from fastapi import Query


from eternalog.api.rate_limit import rate_limiter, cache_get, cache_set, make_cache_key  # pyright: ignore [reportMissingImports]


@router.get(
    "/log_entries",
    response_model=api_schemas.PaginatedLogEntries,
    responses={
        400: {"model": api_schemas.ErrorResponse},
        404: {"model": api_schemas.ErrorResponse},
        429: {"model": api_schemas.ErrorResponse},
    },
)
def get_all_log_entries(
    request: Request,
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
    limit: int = Query(50, ge=1, le=100, description="Max items per page (1-100)"),
    offset: int = Query(0, ge=0, description="Zero-based offset"),
    content_substr: str | None = Query(
        None, description="Case-insensitive substring match on content"
    ),
    start_ts: datetime.datetime | None = Query(
        None, description="Filter entries with timestamp >= start_ts"
    ),
    end_ts: datetime.datetime | None = Query(
        None, description="Filter entries with timestamp <= end_ts"
    ),
    sort_field: str = Query(
        "created_at",
        pattern="^(created_at|updated_at|timestamp)$",
        description="Field to sort by",
    ),
    sort_dir: str = Query("desc", pattern="^(asc|desc)$", description="Sort direction"),
) -> api_schemas.PaginatedLogEntries:
    """Get paginated log entries with optional filters and sorting.

    Examples:
    - Basic page: /api/v1/log_entries?limit=20
    - Filter substring: /api/v1/log_entries?content_substr=error
    - Date range: /api/v1/log_entries?start_ts=2025-01-01T00:00:00&end_ts=2025-01-31T23:59:59
    - Sort ascending by timestamp: /api/v1/log_entries?sort_field=timestamp&sort_dir=asc
    """
    rate_limiter(request)  # rate limit per API key
    cache_key = make_cache_key(
        limit=limit,
        offset=offset,
        content_substr=content_substr or "",
        start_ts=start_ts or "",
        end_ts=end_ts or "",
        sort_field=sort_field,
        sort_dir=sort_dir,
    )
    cached = cache_get(cache_key)
    if cached:
        return cached
    entries, total = data_core.log_entry_search(
        db,
        limit=limit,
        offset=offset,
        content_substr=content_substr,
        start_ts=start_ts,
        end_ts=end_ts,
        sort_field=sort_field,
        sort_dir=sort_dir,
    )
    response = api_schemas.PaginatedLogEntries(
        items=[
            api_schemas.LogEntryOut(
                id=e.id,
                created_at=e.created_at,
                updated_at=e.updated_at,
                content=e.content,
                timestamp=e.timestamp,
            )
            for e in entries
        ],
        total=total,
        limit=limit,
        offset=offset,
    )
    cache_set(cache_key, response)
    return response


@router.get("/log_entries/{log_entry_id}", response_model=api_schemas.LogEntryOut)
def get_log_entry(
    log_entry_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
) -> api_schemas.LogEntryOut:
    """Get a specific log entry by ID."""
    entry = data_core.log_entry_get(db, log_entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return api_schemas.LogEntryOut(
        id=entry.id,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        content=entry.content,
        timestamp=entry.timestamp,
    )


@router.post("/log_entries", response_model=api_schemas.LogEntryOut)
def create_log_entry(
    log_entry: api_schemas.LogEntryIn,
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
) -> api_schemas.LogEntryOut:
    """Create a new log entry."""
    entry = data_core.log_entry_create(
        db, content=log_entry.content, timestamp=log_entry.timestamp
    )
    return api_schemas.LogEntryOut(
        id=entry.id,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        content=entry.content,
        timestamp=entry.timestamp,
    )


@router.put("/log_entries/{log_entry_id}", response_model=api_schemas.LogEntryOut)
def update_log_entry(
    log_entry_id: uuid.UUID,
    log_entry: api_schemas.LogEntryIn,
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
) -> api_schemas.LogEntryOut:
    """Update an existing log entry."""
    entry = data_core.log_entry_update(
        db,
        log_entry_id,
        content=log_entry.content,
        timestamp=log_entry.timestamp,
    )
    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    return api_schemas.LogEntryOut(
        id=entry.id,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        content=entry.content,
        timestamp=entry.timestamp,
    )


@router.delete("/log_entries/{log_entry_id}", response_model=api_schemas.LogEntryOut)
def delete_log_entry(
    log_entry_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
) -> api_schemas.LogEntryOut:
    """Delete a log entry by ID and return it."""
    entry = data_core.log_entry_get(db, log_entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Log entry not found")
    # capture details before delete
    deleted_schema = api_schemas.LogEntryOut(
        id=entry.id,
        created_at=entry.created_at,
        updated_at=entry.updated_at,
        content=entry.content,
        timestamp=entry.timestamp,
    )
    success = data_core.log_entry_delete(db, log_entry_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete log entry")
    return deleted_schema
