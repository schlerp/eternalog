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
