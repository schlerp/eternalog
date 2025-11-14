# AGENTS.md
Guidance for agentic coding in this repo (root scope).

1. Setup: use Python 3.12; install deps via `uv sync` (or `pip install -e .`); run `pre-commit install`.
2. Run app (hot reload): `make run-develop-native` or Docker `make run-develop`.
3. Full test suite: `make run-tests-native` (runs `pytest -vvv` inside `src`).
4. Single test: from repo root `pytest -vvv src/tests/unit/domain/test_core.py::test_some_case` (or `cd src && pytest path::TestClass::test_name`).
5. Changed tests only: `pytest --picked`; watch mode: `make run-tests-native-loop` (uses `ptw --testmon`).
6. Lint (static + security): `ruff check .`; format: `ruff format .`; type-check: `pyright`; all hooks: `pre-commit run --all-files`.
7. Imports: Ruff isort single-line enforced; order stdlib, third-party, local `eternalog.*`; prefer absolute over relative beyond same package.
8. Style: 88 char lines; 4-space indent; double quotes; trailing commas allowed; no trailing whitespace (hook enforces).
9. Types: target py312; use modern unions (`X | None`); annotate public function params & returns; allow `_var` unused per Ruff config.
10. Naming: snake_case modules/functions; PascalCase classes; UPPER_SNAKE constants; private prefix `_`; avoid one-letter names.
11. Errors: raise precise built-ins (`ValueError`, `TypeError`) or domain-specific; in FastAPI endpoints return/raise `HTTPException`; never swallow exceptions—log with `loguru` then rethrow if needed.
12. Logging: use `loguru` (already a dependency); avoid print(); include context not secrets.
13. Security: Ruff S rules active—avoid `eval`, weak crypto, and non-cryptographic RNG for secrets.
14. Tests: no global state mutation; prefer explicit fixtures; assertions allowed (S101 ignored in tests); magic numbers acceptable only in tests.
15. Data models: keep SQLAlchemy models in `data/models.py`; avoid circular imports—place shared schemas in `domain/schemas.py`.
16. Imports grouping: one import per line (force-single-line); combine from-imports only if same module; avoid wildcard imports.
17. Formatting: rely solely on Ruff (no Black); do not manually align with spaces.
18. Dead code: remove unused vars (excluding underscore-prefixed); Ruff F841 enforced.
19. Docs: add concise docstrings for public APIs (imperative mood); keep examples under 88 cols.
20. Cursor/Copilot rules: none present; follow this file plus Ruff/Pyright configs.
