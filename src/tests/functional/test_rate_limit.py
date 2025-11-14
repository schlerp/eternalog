from fastapi.testclient import TestClient
from eternalog.main import app

API_HEADERS = {"X-API-Key": "dev-key"}


def test_rate_limit_exhaustion() -> None:
    with TestClient(app) as client:
        # assuming limit 30 per minute
        successes = 0
        for i in range(35):
            r = client.get("/api/v1/log_entries", headers=API_HEADERS)
            if r.status_code == 429:
                assert successes >= 1  # some succeeded before limit
                break
            else:
                successes += 1
        else:  # no break encountered
            assert False, "Expected rate limiting did not occur"
