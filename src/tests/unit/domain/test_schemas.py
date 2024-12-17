import datetime
import uuid

from eternalog.domain import schemas


class TestSchemas:
    def test_eternalog_schema_with_known_id(self) -> None:
        uuid_value = uuid.uuid4()

        assert schemas.EternalogSchema(id=uuid_value).id == uuid_value

    def test_eternalog_schema_with_unknown_id(self) -> None:
        assert schemas.EternalogSchema().id is not None

    def test_database_mixin(self) -> None:
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        database_mixin = schemas.DatabaseMixin(
            created_at=created_at, updated_at=updated_at
        )

        assert database_mixin.created_at == created_at
        assert database_mixin.updated_at == updated_at

    def test_log_entry(self) -> None:
        message = "Test message"
        timestamp = datetime.datetime.now()

        log_entry = schemas.LogEntry(message=message, timestamp=timestamp)

        assert log_entry.id is not None
        assert log_entry.message == message
        assert log_entry.timestamp == timestamp

    def test_log_entry_database(self) -> None:
        message = "Test message"
        timestamp = datetime.datetime.now()
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        log_entry = schemas.LogEntryDatabase(
            message=message,
            timestamp=timestamp,
            created_at=created_at,
            updated_at=updated_at,
        )

        assert log_entry.id is not None
        assert log_entry.message == message
        assert log_entry.timestamp == timestamp
        assert log_entry.created_at == created_at
        assert log_entry.updated_at == updated_at

    def test_block_schema(self) -> None:
        timestamp = datetime.datetime.now()
        message = "Test content"
        signature = b"Test signature"
        parent_block = None

        block = schemas.BlockSchema(
            timestamp=timestamp,
            message=message,
            signature=signature,
            parent_block=parent_block,
        )

        assert block.timestamp == timestamp
        assert block.message == message
        assert block.signature == signature
        assert block.parent_block == parent_block

    def test_block_schema_database(self) -> None:
        timestamp = datetime.datetime.now()
        message = "Test content"
        signature = b"Test signature"
        parent_block = None
        created_at = datetime.datetime.now()
        updated_at = datetime.datetime.now()

        block = schemas.BlockSchemaDatbase(
            timestamp=timestamp,
            message=message,
            signature=signature,
            parent_block=parent_block,
            created_at=created_at,
            updated_at=updated_at,
        )

        assert block.timestamp == timestamp
        assert block.message == message
        assert block.signature == signature
        assert block.parent_block == parent_block
        assert block.created_at == created_at
        assert block.updated_at == updated_at
