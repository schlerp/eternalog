from fastapi.testclient import TestClient
from eternalog.main import app

API_HEADERS = {"X-API-Key": "dev-key"}


def test_error_response_contains_ids() -> None:
    with TestClient(app, raise_server_exceptions=False) as client:
        r = client.get("/api/v1/test/error", headers=API_HEADERS)
        assert r.status_code == 500
        data = r.json()
        assert "request_id" in data
        assert "correlation_id" in data
        assert data["request_id"]
        assert data["correlation_id"]
        assert data["code"] == "internal_error"
        assert data["detail"] == "forced test error"
