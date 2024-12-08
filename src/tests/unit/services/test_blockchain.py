import uuid

import pytest

from eternalog.domain import core
from eternalog.services import blockchain as blockchain_service


class TestBlockchainService:
    def test_add_block(self):
        service = blockchain_service.BlockchainService(name="test")
        block = service.add_block(b"Hello, World!")
        assert block.content == b"Hello, World!"
        assert block.parent_block == service.starting_block

    def test_get_latest_block(self):
        service = blockchain_service.BlockchainService(name="test")

        block: core.Block | None = None
        for i in range(3):
            block = service.add_block(f"Block {i}".encode("utf-8"))

        assert block is not None
        assert service.get_latest_block() == block

    def test_get_block(self):
        service = blockchain_service.BlockchainService(name="test")
        block: core.Block | None = None
        for i in range(3):
            block = service.add_block(f"Block {i}".encode("utf-8"))

        assert block is not None
        assert service.get_block(block.id) == block

    def test_get_block_raises_block_not_found_error(self):
        service = blockchain_service.BlockchainService(name="test")
        block: core.Block | None = None
        for i in range(3):
            block = service.add_block(f"Block {i}".encode("utf-8"))

        assert block is not None
        with pytest.raises(blockchain_service.BlockNotFoundError):
            service.get_block(uuid.uuid4())

    def test_get_block_raises_block_not_found_error_for_genesis_block(self):
        service = blockchain_service.BlockchainService(name="test")
        with pytest.raises(blockchain_service.BlockNotFoundError):
            service.get_block(uuid.uuid4())
