from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest


def test_build_postgres_url_uses_env_and_encodes_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange: set env vars (including special chars to verify URL encoding)
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "trading_platform")
    monkeypatch.setenv("DB_USER", "user@example.com")
    monkeypatch.setenv("DB_PASSWORD", "p@ss:word/with?chars")

    # Import after env vars are set so settings pick them up
    import core.db as db

    # Act
    url = db.build_postgres_url()

    # Assert: core shape
    assert url.startswith("postgresql+psycopg2://")
    assert "@localhost:5432/trading_platform" in url

    # Assert: credentials are URL-encoded (not raw)
    assert "user%40example.com" in url  # @ -> %40
    assert "p%40ss%3Aword%2Fwith%3Fchars" in url  # @ : / ? encoded


def test_create_db_engine_returns_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange: minimal env vars
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "trading_platform")
    monkeypatch.setenv("DB_USER", "postgres")
    monkeypatch.setenv("DB_PASSWORD", "postgres")

    import core.db as db

    # Patch create_engine so we don't require psycopg2 to be installed
    fake_engine = MagicMock()
    fake_engine.url = "postgresql+psycopg2://postgres:postgres@localhost:5432/trading_platform"

    def _fake_create_engine(url: str, **kwargs: Any) -> Any:
        # Validate that db.create_db_engine passes the expected URL
        assert url.endswith("/trading_platform")
        return fake_engine

    monkeypatch.setattr(db, "create_engine", _fake_create_engine)

    # Act
    engine = db.create_db_engine()

    # Assert
    assert engine is fake_engine
    assert str(engine.url).endswith("/trading_platform")
