import datetime
import uuid

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
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


@router.get("/log_entries", response_model=api_schemas.PaginatedLogEntries)
def get_all_log_entries(
    db: Session = Depends(get_db),
    _: str = Depends(api_key_auth),
    limit: int = 50,
    offset: int = 0,
    content_substr: str | None = None,
    start_ts: datetime.datetime | None = None,
    end_ts: datetime.datetime | None = None,
    sort_field: str = "created_at",
    sort_dir: str = "desc",
) -> api_schemas.PaginatedLogEntries:
    """Get paginated log entries with optional filters and sorting."""
    if limit > 100 or limit <= 0:
        raise HTTPException(status_code=400, detail="limit out of range (1-100)")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be >= 0")
    if sort_dir.lower() not in {"asc", "desc"}:
        raise HTTPException(status_code=400, detail="sort_dir must be 'asc' or 'desc'")
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
    return api_schemas.PaginatedLogEntries(
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
