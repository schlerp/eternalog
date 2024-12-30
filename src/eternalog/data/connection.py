import typing
from contextlib import contextmanager

from sqlalchemy import Engine
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from eternalog.data import config


def get_engine() -> Engine:
    db_engine = create_engine(config.SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

    if not database_exists(db_engine.url):
        create_database(db_engine.url)

    return db_engine


engine = get_engine()
SessionFactory = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)


@contextmanager
def get_db_session() -> typing.Generator[Session]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
