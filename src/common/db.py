from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from src.common.config import settings


def build_postgres_url() -> str:
    """
    Build a safe SQLAlchemy PostgreSQL URL from environment-backed settings.
    """
    user = quote_plus(settings.db_user)
    password = quote_plus(settings.db_password)
    host = settings.db_host
    port = settings.db_port
    db = settings.db_name
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"


def create_db_engine() -> Engine:
    """
    Create a SQLAlchemy engine.
    - pool_pre_ping helps with stale connections (useful in serverless/container environments).
    """
    url = build_postgres_url()
    return create_engine(url, pool_pre_ping=True)


engine: Engine = create_db_engine()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    """
    Provide a transactional scope around a series of operations.

    Usage:
        from src.common.db import session_scope

        with session_scope() as s:
            s.execute(...)
    """
    session: Session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
