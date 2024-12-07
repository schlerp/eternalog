from __future__ import annotations

import datetime
import uuid

import pydantic


class EternalogSchema(pydantic.BaseModel):
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)


class DatabaseMixin(pydantic.BaseModel):
    created_at: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = pydantic.Field(
        default_factory=datetime.datetime.now
    )

    model_config = pydantic.ConfigDict(from_attributes=True)


class LogEntry(EternalogSchema):
    message: str
    timestamp: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)


class LogEntryDatabase(LogEntry, DatabaseMixin):
    pass


class BlockSchema(LogEntry):
    signature: bytes
    parent_block: BlockSchema | None


class BlockSchemaDatbase(BlockSchema, DatabaseMixin):
    pass
