from fastapi.testclient import TestClient
from eternalog.main import app
from eternalog.data import connection, core as data_core

API_HEADERS = {"X-API-Key": "dev-key"}


def setup_module(module):  # noqa: ANN001
    data_core.create_all(connection.engine)
    with connection.get_db_session() as db:
        import datetime

        for i in range(30):
            data_core.log_entry_create(
                db, content=f"msg-{i}", timestamp=datetime.datetime.now()
            )  # type: ignore[arg-type]


def test_pagination_limits() -> None:
    with TestClient(app) as client:
        resp = client.get("/api/v1/log_entries?limit=10&offset=0", headers=API_HEADERS)
        assert resp.status_code == 200
        body = resp.json()
        assert body["limit"] == 10
        assert body["offset"] == 0
        assert body["total"] >= 30
        assert len(body["items"]) == 10

        resp2 = client.get(
            "/api/v1/log_entries?limit=10&offset=10", headers=API_HEADERS
        )
        body2 = resp2.json()
        assert body2["offset"] == 10
        assert len(body2["items"]) == 10

        resp3 = client.get(
            "/api/v1/log_entries?limit=10&offset=20", headers=API_HEADERS
        )
        body3 = resp3.json()
        assert body3["offset"] == 20
        # last page may have 10 or fewer depending on seed
        assert len(body3["items"]) <= 10
