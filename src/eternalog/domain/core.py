from __future__ import annotations

from eternalog.domain import config, schemas
import binascii
from datetime import datetime
from typing import Optional, override

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


def get_private_key() -> rsa.RSAPrivateKey:
    return config.PRIVATE_KEY


def get_public_key() -> rsa.RSAPublicKey:
    return config.PUBLIC_KEY


def sign(data: bytes, privkey: rsa.RSAPrivateKey) -> bytes:
    return privkey.sign(
        data=data,
        padding=padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
        ),
        algorithm=hashes.SHA256(),
    )


def verify(data: bytes, signature: bytes, pubkey: rsa.RSAPublicKey) -> bool:
    try:
        pubkey.verify(
            data=data,
            signature=signature,
            padding=padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            algorithm=hashes.SHA256(),
        )
        return True
    except InvalidSignature:
        return False


class Block:
    def __init__(self, content: bytes = b"", parent_block: Block | None = None):
        self.timestamp = datetime.now()
        self.content = content
        self.parent_block: Block | None = parent_block
        self.signature = self._sign()

    def get_signature(self) -> str:
        return binascii.hexlify(self.signature).decode("utf-8")

    def get_hash(self) -> bytes:
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data=self.timestamp.isoformat().encode("utf-8"))
        digest.update(data=self.content)
        if self.parent_block is not None:
            digest.update(data=self.parent_block.get_hash())
        return digest.finalize()

    def get_timestamp(self) -> str:
        return self.timestamp.isoformat()

    def get_content(self) -> str:
        return self.content.decode("utf-8")

    def get_parent_block(self) -> Optional["BlockChain"]:
        return self.parent_block

    def _sign(self) -> bytes:
        return sign(data=self.get_hash(), privkey=get_private_key())

    def verify(self) -> bool:
        return verify(
            data=self.get_hash(),
            signature=self.signature,
            pubkey=get_public_key(),
        )

    def walk_blocks(self) -> list["BlockChain"]:
        current_block = self
        blocks = []
        while True:
            blocks.append(current_block)
            if current_block.parent_block:
                current_block = current_block.parent_block  # type: ignore
            else:
                break
        return list(reversed(blocks))

    def __repr__(self) -> str:
        ret = f"\n{self.__class__.__name__}"
        ret += f"\n             timestamp: {self.get_timestamp()}"
        ret += f"\n               content: {self.get_content()}"
        ret += f"\n             signature: {self.get_signature()[:32]}"
        ret += f"\n               verifed: {self.verify()}"
        if self.parent_block:
            ret += f"\nparent block timestamp: {self.parent_block.get_timestamp()}"
            ret += f"\nparent block signature: {self.parent_block.get_signature()[:32]}"
        return ret

    def __str__(self) -> str:
        return self.__repr__()
