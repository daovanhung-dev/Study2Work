import pytest
from app.core import constants
from app.core.config import Settings
from app.core.responses import _ApiError


def test_settings_defaults_come_from_constants() -> None:
    """Kiểm tra Settings lấy app environment, CORS, database URL, Redis và các giá trị JWT mặc định
    từ app.core.constants."""
    settings = Settings()

    assert settings.app_env == constants.APP_ENV
    assert settings.enable_docs == constants.ENABLE_DOCS
    assert settings.cors_origins == list(constants.CORS_ORIGINS)
    assert settings.cors_origins == ["http://127.0.0.2:3002", "http://127.0.0.2:3001"]
    assert settings.URL_DATABASE == constants.URL_DATABASE
    assert settings.db_host is None
    assert settings.db_port is None
    assert settings.db_name is None
    assert settings.db_user is None
    assert settings.DB_PASSWORD is None
    assert settings.db_schema == constants.DB_SCHEMA
    assert settings.redis_url == constants.REDIS_URL
    assert settings.jwt_algorithm == constants.JWT_ALGORITHM
    assert settings.jwt_access_token_expire_minutes == constants.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    assert settings.jwt_refresh_token_expire_days == constants.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    assert settings.jwt_issuer == constants.JWT_ISSUER
    assert settings.jwt_audience == constants.JWT_AUDIENCE


def test_settings_ignore_environment_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra khởi tạo Settings không tự đọc biến môi trường của tiến trình và vẫn dùng các hằng
    số runtime đã khai báo."""
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DB_HOST", "environment-host")
    monkeypatch.setenv("URL_DATABASE", "postgresql://environment-host/environment-db")
    monkeypatch.setenv("JWT_ALGORITHM", "HS256")

    settings = Settings()

    assert settings.app_env == constants.APP_ENV
    assert settings.URL_DATABASE == constants.URL_DATABASE
    assert settings.db_host is None
    assert settings.jwt_algorithm == constants.JWT_ALGORITHM


def test_settings_accept_legacy_constructor_aliases() -> None:
    """Kiểm tra Settings tiếp tục nhận tên trường viết hoa cũ khi caller truyền cấu hình tường minh
    vào constructor."""
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
    assert settings.URL_DATABASE == constants.URL_DATABASE


def test_settings_reject_unsafe_database_schema() -> None:
    """Kiểm tra schema chứa ký tự không được phép bị từ chối và được chuyển thành lỗi API nội bộ an
    toàn."""
    with pytest.raises(_ApiError) as error:
        Settings(
            db_host="localhost",
            db_name="study",
            db_user="user",
            db_password="password",
            db_schema="study;drop table users",
            jwt_algorithm="HS256",
            jwt_secret_key="test-secret-key-that-is-at-least-32-characters",
        )

    assert error.value.status_code == 500
    assert error.value.business_code == "INTERNAL_SERVER_ERROR"
    assert "drop table" not in error.value.message


def test_es256_requires_private_key() -> None:
    """Kiểm tra cấu hình ES256 thiếu private key bị từ chối thay vì tạo Settings không thể ký
    access token."""
    with pytest.raises(_ApiError):
        Settings(jwt_algorithm="ES256", jwt_private_key=None)
