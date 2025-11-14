from fastapi.testclient import TestClient
from eternalog.main import app


def test_health_info_contains_commit_and_start_time() -> None:
    with TestClient(app) as client:
        r = client.get("/health/info")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "ok"
        assert "commit" in data and data["commit"]
        assert "start_time" in data and data["start_time"].startswith("20")
