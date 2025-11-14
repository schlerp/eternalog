from fastapi.testclient import TestClient

from eternalog.main import app
from eternalog.data import core as data_core
from eternalog.data import connection

API_HEADERS = {"X-API-Key": "dev-key"}


def setup_module(module):  # noqa: ANN001
    # ensure tables exist
    data_core.create_all(connection.engine)


class TestLogEntryRouter:
    def test_create_and_get_log_entry(self) -> None:
        with TestClient(app) as client:
            payload = {"content": "hello", "timestamp": "2024-01-01T00:00:00"}
            create_response = client.post(
                "/api/v1/log_entries", json=payload, headers=API_HEADERS
            )
            assert create_response.status_code == 200
            created = create_response.json()
            entry_id = created["id"]

            get_response = client.get(
                f"/api/v1/log_entries/{entry_id}", headers=API_HEADERS
            )
            assert get_response.status_code == 200
            fetched = get_response.json()
            assert fetched["content"] == "hello"

    def test_list_log_entries(self) -> None:
        with TestClient(app) as client:
            list_response = client.get("/api/v1/log_entries", headers=API_HEADERS)
            assert list_response.status_code == 200
            assert isinstance(list_response.json(), list)

    def test_update_log_entry(self) -> None:
        with TestClient(app) as client:
            payload = {"content": "hello", "timestamp": "2024-01-01T00:00:00"}
            create_response = client.post(
                "/api/v1/log_entries", json=payload, headers=API_HEADERS
            )
            assert create_response.status_code == 200
            entry_id = create_response.json()["id"]

            update_payload = {
                "content": "updated",
                "timestamp": "2024-01-02T00:00:00",
            }
            update_response = client.put(
                f"/api/v1/log_entries/{entry_id}",
                json=update_payload,
                headers=API_HEADERS,
            )
            assert update_response.status_code == 200
            assert update_response.json()["content"] == "updated"

    def test_delete_log_entry(self) -> None:
        with TestClient(app) as client:
            payload = {"content": "hello", "timestamp": "2024-01-01T00:00:00"}
            create_response = client.post(
                "/api/v1/log_entries", json=payload, headers=API_HEADERS
            )
            assert create_response.status_code == 200
            entry_id = create_response.json()["id"]

            delete_response = client.delete(
                f"/api/v1/log_entries/{entry_id}", headers=API_HEADERS
            )
            assert delete_response.status_code == 200
            deleted = delete_response.json()
            assert deleted["id"] == entry_id

            get_response = client.get(
                f"/api/v1/log_entries/{entry_id}", headers=API_HEADERS
            )
            assert get_response.status_code == 404
