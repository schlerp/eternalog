from fastapi.testclient import TestClient
from eternalog.main import app


class TestHealthRouter:
    def test_live(self) -> None:
        with TestClient(app) as client:
            resp = client.get("/health/live")
            assert resp.status_code == 200
            assert resp.json()["status"] == "ok"

    def test_ready(self) -> None:
        with TestClient(app) as client:
            resp = client.get("/health/ready")
            assert resp.status_code == 200
            body = resp.json()
            assert body["status"] == "ok"
            assert "time" in body
