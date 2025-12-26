import importlib

import pytest


def test_build_postgres_url_uses_env_and_encodes_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange: set env vars (including special chars to verify URL encoding)
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")
    monkeypatch.setenv("DB_NAME", "trading_platform")
    monkeypatch.setenv("DB_USER", "user@example.com")
    monkeypatch.setenv("DB_PASSWORD", "p@ss:word/with?chars")

    # Important: reload modules so they pick up env var changes
    import src.common.config as config
    import src.common.db as db

    importlib.reload(config)
    importlib.reload(db)

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

    import src.common.config as config
    import src.common.db as db

    importlib.reload(config)
    importlib.reload(db)

    # Act
    engine = db.create_db_engine()

    # Assert
    assert engine is not None
    assert str(engine.url).endswith("/trading_platform")