from sqlalchemy import MetaData
from sqlalchemy.orm import registry
from sqlalchemy.orm import Session

from eternalog.data import models

metadata = MetaData()
mapper_registry = registry()


def create_all(engine) -> None:  # type: ignore[no-untyped-def]
    models.Base.metadata.create_all(bind=engine)


# LogEntry CRUD helpers


def log_entry_create(db: Session, *, content: str, timestamp) -> models.LogEntry:  # type: ignore[no-untyped-def]
    entry = models.LogEntry(content=content, timestamp=timestamp)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def log_entry_get(db: Session, entry_id) -> models.LogEntry | None:  # type: ignore[no-untyped-def]
    return db.query(models.LogEntry).filter(models.LogEntry.id == entry_id).first()


def log_entry_list(
    db: Session, limit: int = 100, offset: int = 0
) -> list[models.LogEntry]:
    return (
        db.query(models.LogEntry)
        .order_by(models.LogEntry.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def log_entry_search(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
    content_substr: str | None = None,
    start_ts=None,
    end_ts=None,
    sort_field: str = "created_at",
    sort_dir: str = "desc",
) -> tuple[list[models.LogEntry], int]:  # type: ignore[no-untyped-def]
    q = db.query(models.LogEntry)
    if content_substr:
        q = q.filter(models.LogEntry.content.ilike(f"%{content_substr}%"))
    if start_ts is not None:
        q = q.filter(models.LogEntry.timestamp >= start_ts)
    if end_ts is not None:
        q = q.filter(models.LogEntry.timestamp <= end_ts)
    total = q.count()
    # validate sort field
    if sort_field not in {"created_at", "updated_at", "timestamp"}:
        sort_field = "created_at"
    col = getattr(models.LogEntry, sort_field)
    if sort_dir.lower() == "asc":
        q = q.order_by(col.asc())
    else:
        q = q.order_by(col.desc())
    items = q.offset(offset).limit(limit).all()
    return items, total


def log_entry_count(db: Session) -> int:  # type: ignore[no-untyped-def]
    return db.query(models.LogEntry).count()


def log_entry_update(
    db: Session, entry_id, *, content: str | None = None, timestamp=None
) -> models.LogEntry | None:  # type: ignore[no-untyped-def]
    entry = log_entry_get(db, entry_id)
    if entry is None:
        return None
    if content is not None:
        entry.content = content
    if timestamp is not None:
        entry.timestamp = timestamp
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def log_entry_delete(db: Session, entry_id) -> bool:  # type: ignore[no-untyped-def]
    entry = log_entry_get(db, entry_id)
    if entry is None:
        return False
    db.delete(entry)
    db.commit()
    return True
