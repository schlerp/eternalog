import time
import threading
from collections import defaultdict
from typing import Any

from fastapi import HTTPException, Request

_lock = threading.Lock()
_buckets: dict[str, dict[str, float]] = defaultdict(dict)  # {id: {tokens, last}}
CACHE_TTL_SECONDS = 10
_cache: dict[str, tuple[float, Any]] = {}

RATE_LIMIT = 30  # requests
WINDOW_SECONDS = 60


def rate_limiter(request: Request) -> None:
    client_id = request.headers.get("X-API-Key", "anon")
    now = time.time()
    with _lock:
        bucket = _buckets.get(client_id)
        if not bucket:
            bucket = {"tokens": RATE_LIMIT, "last": now}
            _buckets[client_id] = bucket
        # refill
        elapsed = now - bucket["last"]
        if elapsed > WINDOW_SECONDS:
            bucket["tokens"] = RATE_LIMIT
            bucket["last"] = now
        if bucket["tokens"] <= 0:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        bucket["tokens"] -= 1


def make_cache_key(**params: Any) -> str:
    return "|".join(f"{k}={v}" for k, v in sorted(params.items()))


def cache_get(key: str):  # type: ignore[no-untyped-def]
    item = _cache.get(key)
    if not item:
        return None
    ts, value = item
    if time.time() - ts > CACHE_TTL_SECONDS:
        del _cache[key]
        return None
    return value


def cache_set(key: str, value):  # type: ignore[no-untyped-def]
    _cache[key] = (time.time(), value)
