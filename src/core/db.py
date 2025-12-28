from __future__ import annotations

from typing import Final
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

_DRIVER: Final[str] = "postgresql+psycopg2"


def build_postgres_url() -> str:
    """
    Build a Postgres SQLAlchemy URL from environment-backed settings.

    Credentials are URL-encoded to safely handle special characters.
    """
    user = quote_plus(settings.db_user)
    password = quote_plus(settings.db_password)
    host = settings.db_host
    port = settings.db_port
    name = settings.db_name

    return f"{_DRIVER}://{user}:{password}@{host}:{port}/{name}"


def create_db_engine() -> Engine:
    """
    Create a SQLAlchemy Engine.

    IMPORTANT: This function should be called explicitly by the composition root
    (app startup), not at import time, so tests/imports don't require psycopg2.
    """
    url = build_postgres_url()
    return create_engine(url, pool_pre_ping=True)


# --- Lazy, cached engine / session factory (safe for imports & tests) ---

_engine: Engine | None = None
SessionLocal = sessionmaker()


def get_engine() -> Engine:
    """
    Lazily create and cache the Engine, and bind the SessionLocal factory.

    This avoids importing DB drivers / connecting during module import.
    """
    global _engine
    if _engine is None:
        _engine = create_db_engine()
        SessionLocal.configure(bind=_engine)
    return _engine
