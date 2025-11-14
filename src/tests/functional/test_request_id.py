from fastapi.testclient import TestClient
from eternalog.main import app

API_HEADERS = {"X-API-Key": "dev-key"}


def test_request_id_generated() -> None:
    with TestClient(app) as client:
        r = client.get("/api/v1/log_entries", headers=API_HEADERS)
        assert r.status_code == 200
        assert "X-Request-ID" in r.headers
        assert r.headers["X-Request-ID"]


def test_request_id_propagated() -> None:
    with TestClient(app) as client:
        hdrs = {**API_HEADERS, "X-Request-ID": "custom-id-123"}
        r = client.get("/api/v1/log_entries", headers=hdrs)
        assert r.status_code == 200
        assert r.headers["X-Request-ID"] == "custom-id-123"
