from fastapi import Depends, Header, HTTPException

API_KEY_HEADER = "X-API-Key"
API_KEY_ENV_VAR = "ETERNALOG_API_KEY"

import os

EXPECTED_KEY = os.getenv(API_KEY_ENV_VAR, "dev-key")


def api_key_auth(x_api_key: str = Header(alias=API_KEY_HEADER)) -> str:  # pyright: ignore [reportInvalidTypeVarUse]
    if x_api_key != EXPECTED_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key
