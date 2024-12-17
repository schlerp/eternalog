import uuid

from loguru import logger

from eternalog.domain import core


class BlockNotFoundError(Exception):
    def __init__(self, block_id: uuid.UUID) -> None:
        self.block_id = block_id
        super().__init__(f"Block with id {block_id} not found.")


class BlockchainService:
    def __init__(self, name: str) -> None:
        self.name = name
        self.starting_block = core.Block(
            content=f"Genesis Block: {self.name}".encode("utf-8"), parent_block=None
        )
        self._latest_block = self.starting_block
        logger.debug(
            f"Created blockchain service: '{self.name}' with genesis block {self.starting_block.id}"
        )

    def add_block(self, content: bytes) -> core.Block:
        """Add a new block to the blockchain."""
        new_block = core.Block(content=content, parent_block=self._latest_block)
        self._latest_block = new_block
        logger.info(f"Added block: {new_block.id}")
        logger.debug(f"Latest block is now: {self._latest_block.id}")
        return new_block

    def get_latest_block(self) -> core.Block:
        """Get the latest block in the blockchain."""
        logger.debug(f"Getting latest block: {self._latest_block.id}")
        return self._latest_block

    def get_block(self, block_id: uuid.UUID) -> core.Block:
        """Get a block by its id or raise a BlockNotFoundError."""
        logger.debug(f"Looking for block: {block_id}")

        current_block = self._latest_block

        exit_loop: bool = False
        while not exit_loop:
            logger.debug(f"Checking block: {current_block.id}")
            if current_block.id == block_id:
                logger.info(f"Found block: {current_block.id}")
                exit_loop = True

            elif current_block.parent_block is None:
                error = BlockNotFoundError(block_id)
                logger.error(f"Block not found: {block_id}")
                raise error

            else:
                logger.debug(f"Moving to parent block: {current_block.parent_block.id}")
                current_block = current_block.parent_block

        return current_block


def load_blockchain_service(name: str) -> BlockchainService:
    # TODO: get this from the database and load the blocks
    return BlockchainService(name=name)
