import os
import tempfile
from pathlib import Path

from sqlalchemy import inspect, create_engine

from eternalog.data import models


def test_migration_cycle() -> None:
    # Use temp sqlite file
    tmp_dir = tempfile.TemporaryDirectory()
    db_path = Path(tmp_dir.name) / "cycle.db"
    os.environ["ETERNALOG_SQLALCHEMY_DATABASE_URL"] = f"sqlite:///{db_path}"

    # Upgrade head
    os.system("alembic upgrade head")
    engine = create_engine(os.environ["ETERNALOG_SQLALCHEMY_DATABASE_URL"])  # type: ignore[arg-type]
    insp = inspect(engine)
    assert set(["block", "log_entry"]).issubset(set(insp.get_table_names()))

    # Downgrade and upgrade again
    os.system("alembic downgrade -1 || true")
    os.system("alembic upgrade head")
    insp2 = inspect(engine)
    assert set(["block", "log_entry"]).issubset(set(insp2.get_table_names()))
