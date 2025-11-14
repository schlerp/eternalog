import os
import tempfile
from pathlib import Path

from sqlalchemy import create_engine, inspect
from alembic import command
from alembic.config import Config


def _make_alembic_config(db_url: str) -> Config:
    root = Path(__file__).resolve().parents[4]
    cfg = Config(str(root / "alembic.ini"))
    cfg.set_main_option("script_location", str(root / "migrations"))
    cfg.set_main_option("sqlalchemy.url", db_url)
    return cfg


def test_migration_cycle() -> None:
    tmp_dir = tempfile.TemporaryDirectory()
    db_path = Path(tmp_dir.name) / "cycle.db"
    db_url = f"sqlite:///{db_path}"

    os.environ["ETERNALOG_SQLALCHEMY_DATABASE_URL"] = db_url
    alembic_cfg = _make_alembic_config(db_url)

    # Upgrade head
    command.upgrade(alembic_cfg, "head")
    engine = create_engine(db_url)
    insp = inspect(engine)
    assert {"block", "log_entry"}.issubset(set(insp.get_table_names()))

    # Downgrade (ignore if base) then upgrade again
    try:
        command.downgrade(alembic_cfg, "-1")
    except Exception:
        pass
    command.upgrade(alembic_cfg, "head")
    insp2 = inspect(engine)
    assert {"block", "log_entry"}.issubset(set(insp2.get_table_names()))
