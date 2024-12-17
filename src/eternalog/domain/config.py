import os
import tempfile
from typing import cast

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

_KEY_PATH = tempfile.gettempdir() + "/private.pem"


def _load_private_key_from_file(path: str) -> rsa.RSAPrivateKey | None:
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return cast(
            rsa.RSAPrivateKey,
            serialization.load_pem_private_key(f.read(), password=None),
        )


def _get_rsa_key() -> rsa.RSAPrivateKey:
    private_key = _load_private_key_from_file(_KEY_PATH)
    if private_key is None:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        with open(_KEY_PATH, "wb") as f:
            f.writelines(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                ).splitlines()
            )
    return private_key


PRIVATE_KEY: rsa.RSAPrivateKey = _get_rsa_key()

PUBLIC_KEY: rsa.RSAPublicKey = PRIVATE_KEY.public_key()
