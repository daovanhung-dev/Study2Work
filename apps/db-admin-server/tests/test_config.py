from __future__ import annotations

from app.core import constants
from app.core.config import Settings, get_settings
from app.core.database import build_engine


def test_runtime_settings_are_loaded_from_constants() -> None:
    settings = get_settings()

    assert settings.database_url.get_secret_value() == constants.URL_DATABASE
    assert settings.app_env == constants.APP_ENV
    assert settings.port == constants.PORT
    assert settings.dev_auth is False
    assert settings.local_auth_enabled is True


def test_build_engine_drops_neon_pgbouncer_hint_for_psycopg() -> None:
    settings = Settings(
        app_env="test",
        database_url=(
            "postgresql://user:password@localhost/database?pgbouncer=true&connect_timeout=30"
        ),
        jwt_issuer="issuer",
        jwt_audience="audience",
        dev_auth=True,
    )

    engine = build_engine(settings)

    assert engine.url.drivername == "postgresql+psycopg"
    assert "pgbouncer" not in engine.url.query
    assert engine.url.query["connect_timeout"] == "30"
    engine.dispose()
