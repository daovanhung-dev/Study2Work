from __future__ import annotations

from app.core import constants
from app.core.config import get_settings


def test_runtime_settings_are_loaded_from_constants() -> None:
    settings = get_settings()

    assert settings.database_url.get_secret_value() == constants.URL_DATABASE
    assert settings.app_env == constants.APP_ENV
    assert settings.port == constants.PORT
    assert settings.dev_auth is True
