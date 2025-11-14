# eternalog

Immutable log storage & blockchain-inspired versioning service.

## Quick Start
1. Python 3.12; install deps: `uv sync` (or `pip install -e .`)
2. Run app (dev): `make run-develop-native` then visit `http://localhost:8000/docs`
3. Run tests: `make run-tests-native` or single test: `pytest -vvv src/tests/functional/test_log_entry_router.py::TestLogEntryRouter::test_create_and_get_log_entry`
4. Lint/format: `ruff check .` / `ruff format .`; types: `pyright`

## Log Entry API
- List: `GET /api/v1/log_entries`
- Get: `GET /api/v1/log_entries/{id}`
- Create: `POST /api/v1/log_entries` (`content`, `timestamp` ISO8601)
- Update: `PUT /api/v1/log_entries/{id}`
- Delete: `DELETE /api/v1/log_entries/{id}` (returns deleted entry)

## Persistence
- SQLite by default (`ETERNALOG_SQLALCHEMY_DATABASE_URL` override env)
- Auto-creates tables on first test usage via `data.core.create_all`
- Migrations: (Alembic planned) run `alembic upgrade head` after configuring (see Alembic README TBD)

## Health Endpoints
- Liveness: `GET /health/live`
- Readiness: `GET /health/ready`

## Auth
- All `/api/v1/log_entries` endpoints require header `X-API-Key: dev-key` (override via env `ETERNALOG_API_KEY`).

## Development Notes
- Use `loguru` for logging; no `print()`.
- Avoid wildcard imports; single-line isort enforced.
- Pydantic models define schemas; ORM models in `data/models.py`.
