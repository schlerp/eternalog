# eternalog

Immutable log storage & blockchain-inspired versioning service.

## Quick Start
1. Python 3.12; install deps: `uv sync` (or `pip install -e .`)
2. Run app (dev): `make run-develop-native` then visit `http://localhost:8000/docs`
3. Run tests: `make run-tests-native` or single test: `pytest -vvv src/tests/functional/test_log_entry_router.py::TestLogEntryRouter::test_create_and_get_log_entry`
4. Lint/format: `ruff check .` / `ruff format .`; types: `pyright`

## Log Entry API
- List: `GET /api/v1/log_entries?limit=<int>&offset=<int>&content_substr=<str>&start_ts=<iso>&end_ts=<iso>&sort_field=<created_at|updated_at|timestamp>&sort_dir=<asc|desc>`
  - Default `limit=50`, `offset=0`; max limit 100; returns `{items, total, limit, offset}`.
  - Rate limit: 30 requests / minute per API key (HTTP 429 on exceed).
  - Examples:
    - Page: `/api/v1/log_entries?limit=25`
    - Substring: `/api/v1/log_entries?content_substr=error`
    - Date range: `/api/v1/log_entries?start_ts=2025-01-01T00:00:00&end_ts=2025-01-31T23:59:59`
    - Sort ascending: `/api/v1/log_entries?sort_field=timestamp&sort_dir=asc`
- Get: `GET /api/v1/log_entries/{id}`
- Create: `POST /api/v1/log_entries` (`content`, `timestamp` ISO8601)
- Update: `PUT /api/v1/log_entries/{id}`
- Delete: `DELETE /api/v1/log_entries/{id}` (returns deleted entry)

## CLI Export
- Script: `scripts/export-log-entries` (run with venv active)
- Example: `python scripts/export-log-entries --limit 200 --content-substr error --output errors.json`

## Persistence
- SQLite by default (`ETERNALOG_SQLALCHEMY_DATABASE_URL` override env)
- Auto-creates tables on first test usage via `data.core.create_all`
- Migrations: Alembic initialized. Common commands:
  - New revision: `alembic revision -m "desc" --autogenerate`
  - Upgrade: `alembic upgrade head`
  - Downgrade last: `alembic downgrade -1`
  - Show history: `alembic history --verbose`

## Health Endpoints
- Liveness: `GET /health/live`
- Readiness: `GET /health/ready`

## Auth
- All `/api/v1/log_entries` endpoints require header `X-API-Key: dev-key` (override via env `ETERNALOG_API_KEY`).

## Development Notes
- Use `loguru` for logging; no `print()`.
- Avoid wildcard imports; single-line isort enforced.
- Pydantic models define schemas; ORM models in `data/models.py`.
