import datetime
from eternalog import schemas


class LogEntryIn(schemas.LogEntry):
    """Schema for creating a new log entry."""

    pass


class LogEntryOut(schemas.LogEntry):
    """Schema for returning a log entry."""

    created_at: datetime.datetime
    updated_at: datetime.datetime
