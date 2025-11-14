from __future__ import annotations

import pydantic

from eternalog import schemas as root_schemas

EternalogSchema = root_schemas.EternalogSchema
DatabaseMixin = root_schemas.DatabaseMixin
LogEntry = root_schemas.LogEntry


class LogEntryDatabase(LogEntry, DatabaseMixin):
    pass


class BlockSchema(LogEntry):
    signature: bytes
    parent_block: BlockSchema | None


class BlockSchemaDatbase(BlockSchema, DatabaseMixin):
    pass
