from fastapi.testclient import TestClient

from eternalog.main import app


class TestTestRouter:
    def test_echo(self) -> None:
        with TestClient(app) as client:
            test_message = "hello"
            response = client.get(f"api/v1/test/echo/{test_message}")
            assert response.status_code == 200
            assert response.json() == {"message": "hello"}
