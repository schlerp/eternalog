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
        assert len(body3["items"]) <= 10

        # limit validation
        bad_limit = client.get("/api/v1/log_entries?limit=1000", headers=API_HEADERS)
        assert bad_limit.status_code == 400
        negative_limit = client.get("/api/v1/log_entries?limit=-1", headers=API_HEADERS)
        assert negative_limit.status_code == 400

        # sort ascending
        asc_resp = client.get(
            "/api/v1/log_entries?limit=5&sort_dir=asc", headers=API_HEADERS
        )
        assert asc_resp.status_code == 200
        asc_items = asc_resp.json()["items"]
        assert len(asc_items) == 5

        # filtering by substring
        filter_resp = client.get(
            "/api/v1/log_entries?content_substr=msg-1", headers=API_HEADERS
        )
        assert filter_resp.status_code == 200
        filt_items = filter_resp.json()["items"]
        assert any("msg-1" in it["content"] for it in filt_items)
