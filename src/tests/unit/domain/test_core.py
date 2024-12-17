from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from eternalog.domain import core


class TestCoreFunctions:
    def test_get_private_key(self) -> None:
        private_key = core.get_private_key()

        assert isinstance(private_key, RSAPrivateKey)
        assert private_key == core.get_private_key()

    def test_get_public_key(self) -> None:
        public_key = core.get_public_key()

        assert isinstance(public_key, RSAPublicKey)
        assert public_key == core.get_public_key()

    def test_sign(self) -> None:
        data = b"Test data"
        private_key = core.get_private_key()

        signature = core.sign(data=data, privkey=private_key)

        assert isinstance(signature, bytes)
        assert len(signature) == 256

    def test_verify(self) -> None:
        data = b"Test data"
        private_key = core.get_private_key()
        public_key = core.get_public_key()

        signature = core.sign(data=data, privkey=private_key)

        assert core.verify(data=data, signature=signature, pubkey=public_key)


class TestBlock:
    def test_block_signature(self) -> None:
        block = core.Block(content=b"Test content")

        assert block.signature is not None

    def test_block_signature_verification(self) -> None:
        block = core.Block(content=b"Test content")

        assert block.verify()

    def test_child_block_verify(self) -> None:
        parent_block = core.Block(content=b"Test content")
        child_block = core.Block(content=b"Test content", parent_block=parent_block)

        assert child_block.verify()

    def test_child_block_verify_edited(self) -> None:
        parent_block = core.Block(content=b"Test content")
        child_block = core.Block(content=b"Test content", parent_block=parent_block)

        child_block.content = b"Edited content"

        assert parent_block.verify()
        assert not child_block.verify()

    def test_chain_partial_verify(self) -> None:
        parent_block = core.Block(content=b"Test content")
        child_block = core.Block(content=b"Test content", parent_block=parent_block)
        child_block_2 = core.Block(content=b"Test content", parent_block=child_block)

        assert parent_block.verify()
        assert child_block.verify()

        child_block.content = b"Edited content"

        assert parent_block.verify()
        assert not child_block.verify()
        assert not child_block_2.verify()
