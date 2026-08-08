import pytest
from app.core.config import Settings
from pydantic import ValidationError


def test_settings_accept_legacy_environment_aliases() -> None:
    settings = Settings(
        APP_ENV="test",
        ENABLE_DOCS=False,
        CORS_ORIGINS="http://localhost:5173, http://localhost:5174",
        DB_HOST="localhost",
        DB_PORT=5432,
        DB_NAME="study",
        DB_USER="user",
        DB_PASSWORD="p@ssword",
        DB_SCHEMA="study_dev0",
        JWT_ALGORITHM="HS256",
        JWT_SECRET_KEY="test-secret-key-that-is-at-least-32-characters",
    )

    assert settings.app_env == "test"
    assert settings.enable_docs is False
    assert settings.cors_origins == ["http://localhost:5173", "http://localhost:5174"]
    assert settings.DB_PASSWORD == "p@ssword"


def test_settings_reject_unsafe_database_schema() -> None:
    with pytest.raises(ValidationError):
        Settings(
            db_host="localhost",
            db_name="study",
            db_user="user",
            db_password="password",
            db_schema="study;drop table users",
            jwt_algorithm="HS256",
            jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
        )
