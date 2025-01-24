from typing import Self

from eternalog.data import models
from eternalog.domain import core


class TestBlockModel:
    def test_block_creates_from_schema(self: Self) -> None:
        block = core.Block(id=None, content="test".encode())
        block_model = models.Block(**block.as_schema().model_dump())

        assert block_model.content == block.content.decode()
        assert block_model.signature == block.signature
        assert block_model.parent_block is None

    def test_block_creates_from_schema_with_parent(self: Self) -> None:
        parent_block = core.Block(id=None, content="parent".encode())
        parent_block_model = models.Block(**parent_block.as_schema().model_dump())
        block = core.Block(id=None, content="test".encode(), parent_block=parent_block)
        block_dict = {
            **block.as_schema().model_dump(),
            "parent_block": parent_block_model,
        }
        block_model = models.Block(**block_dict)

        assert block_model.content == block.content.decode()
        assert block_model.signature == block.signature
        assert block_model.parent_block is not None
        assert block_model.parent_block.content == parent_block.content.decode()
        assert block_model.parent_block.signature == parent_block.signature
        assert block_model.parent_block.parent_block is None
