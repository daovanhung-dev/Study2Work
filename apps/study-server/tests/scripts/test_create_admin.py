from __future__ import annotations

from unittest.mock import MagicMock, Mock

import pytest
from app.core.config import Settings
from app.core.responses import ErrorDetail
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from scripts import create_admin


def valid_environment() -> dict[str, str]:
    """Tạo cấu hình PostgreSQL local rõ ràng dùng riêng cho kiểm thử CLI."""

    return {
        "STUDY_ADMIN_DATABASE_URL": "postgresql://test-user:test-password@localhost:5432/study_test",
        "STUDY_ADMIN_DB_SCHEMA": "study_test",
        "STUDY_ADMIN_APP_ENV": "test",
    }


def test_load_explicit_settings_requires_all_target_values() -> None:
    """Từ chối thiếu URL/schema/environment thay vì dùng database mặc định của ứng dụng."""

    with pytest.raises(create_admin.AdminBootstrapError, match="STUDY_ADMIN_DATABASE_URL"):
        create_admin.load_explicit_settings({})


def test_load_explicit_settings_uses_postgresql_target_and_schema() -> None:
    """Tạo Settings từ đúng cấu hình tường minh được truyền vào."""

    settings = create_admin.load_explicit_settings(valid_environment())

    assert settings.app_env == "test"
    assert settings.db_schema == "study_test"
    assert settings.database_url.get_secret_value().endswith("/study_test")


def test_load_explicit_settings_rejects_non_postgresql_url() -> None:
    """Không cho script chạy với driver database khác PostgreSQL."""

    environment = valid_environment()
    environment["STUDY_ADMIN_DATABASE_URL"] = "sqlite:///study.db"

    with pytest.raises(create_admin.AdminBootstrapError, match="PostgreSQL"):
        create_admin.load_explicit_settings(environment)


def test_production_requires_explicit_flag() -> None:
    """Chặn production khi người vận hành chưa truyền cờ cho phép."""

    settings = Settings(app_env="production", jwt_algorithm="HS256", jwt_secret_key="x" * 32)

    with pytest.raises(create_admin.AdminBootstrapError, match="--allow-production"):
        create_admin.ensure_environment_allowed(settings, allow_production=False)

    create_admin.ensure_environment_allowed(settings, allow_production=True)


def test_confirm_target_redacts_database_credentials(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Hiển thị host/database/schema nhưng không lộ user hoặc password trong URL."""

    settings = Settings(app_env="local", jwt_algorithm="HS256", jwt_secret_key="x" * 32)
    engine = Mock()
    engine.url = make_url("postgresql://secret-user:secret-password@db.example:5432/study")
    monkeypatch.setattr("builtins.input", lambda _prompt: "CREATE ADMIN")

    assert create_admin.confirm_target(settings, engine, "study_db", "study_schema") is True
    output = capsys.readouterr().out
    assert "db.example:5432" in output
    assert "study_db" in output
    assert "study_schema" in output
    assert "secret-user" not in output
    assert "secret-password" not in output


def test_production_confirmation_requires_production_phrase(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yêu cầu cụm từ production riêng dù cờ cho phép production đã được truyền."""

    settings = Settings(app_env="production", jwt_algorithm="HS256", jwt_secret_key="x" * 32)
    engine = Mock()
    engine.url = make_url("postgresql://db.example/study")
    monkeypatch.setattr("builtins.input", lambda _prompt: "CREATE ADMIN")

    assert create_admin.confirm_target(settings, engine, "study_db", "study_schema") is False


def test_prepare_admin_account_normalizes_fields_and_hashes_password(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trim tên, chuẩn hóa email và chỉ trả password hash thay vì mật khẩu gốc."""

    monkeypatch.setattr(create_admin, "hash_password", lambda _password: "argon2id-hash")

    name, email, password_hash = create_admin.prepare_admin_account(
        "  Admin Person  ",
        " admin@example.com ",
        "a non-empty password",
    )

    assert name == "Admin Person"
    assert email == "admin@example.com"
    assert password_hash == "argon2id-hash"


@pytest.mark.parametrize(
    ("full_name", "email", "password"),
    [
        ("  ", "admin@example.com", "password"),
        ("A" * 151, "admin@example.com", "password"),
        ("Admin", "not-an-email", "password"),
        ("Admin", "admin@example.com", "  "),
    ],
)
def test_prepare_admin_account_rejects_invalid_fields(
    full_name: str,
    email: str,
    password: str,
) -> None:
    """Từ chối tên/email/mật khẩu không đạt các rule hiện có của API đăng ký."""

    with pytest.raises(create_admin.AdminBootstrapError):
        create_admin.prepare_admin_account(full_name, email, password)


def test_prepare_admin_account_maps_email_validation_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ánh xạ an toàn lỗi chuẩn hóa email về lỗi CLI."""

    monkeypatch.setattr(
        create_admin,
        "normalize_email",
        lambda *_args, **_kwargs: ErrorDetail(code="VALUE_ERROR", message="bad email"),
    )

    with pytest.raises(create_admin.AdminBootstrapError, match="Email"):
        create_admin.prepare_admin_account("Admin", "bad", "password")


def test_create_admin_account_inserts_active_admin_with_bound_hash() -> None:
    """Kiểm tra duplicate lookup rồi insert tham số hóa với role/status Admin đang hoạt động."""

    session = Mock()
    session.execute.side_effect = [
        Mock(scalar_one_or_none=Mock(return_value=None)),
        Mock(scalar_one=Mock(return_value=42)),
    ]

    user_id = create_admin.create_admin_account(
        session,
        full_name="Admin Person",
        email="admin@example.com",
        password_hash="argon2id-hash",
    )

    assert user_id == 42
    assert session.execute.call_count == 2
    insert_statement, params = session.execute.call_args.args
    assert "'ADMIN'" in str(insert_statement)
    assert "'ACTIVE'" in str(insert_statement)
    assert params == {
        "full_name": "Admin Person",
        "email": "admin@example.com",
        "password_hash": "argon2id-hash",
    }


def test_create_admin_account_rejects_duplicate_without_insert() -> None:
    """Dừng ngay khi email tồn tại và không chạy câu INSERT thay role hoặc password."""

    session = Mock()
    session.execute.return_value.scalar_one_or_none.return_value = 8

    with pytest.raises(create_admin.DuplicateAdminEmailError, match="không thay đổi"):
        create_admin.create_admin_account(
            session,
            full_name="Admin Person",
            email="admin@example.com",
            password_hash="argon2id-hash",
        )

    assert session.execute.call_count == 1


def test_duplicate_email_transaction_preserves_existing_account() -> None:
    """Kiểm tra duplicate không đổi role/hash của tài khoản và transaction rollback an toàn."""

    engine = create_engine("sqlite:///:memory:")
    try:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY,
                        full_name TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        password_hash TEXT NOT NULL,
                        role TEXT NOT NULL,
                        avatar_url TEXT,
                        phone TEXT,
                        status TEXT,
                        created_at TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP NOT NULL
                    )
                    """
                )
            )

        with Session(engine) as session:
            with session.begin():
                create_admin.create_admin_account(
                    session,
                    full_name="First Admin",
                    email="admin@example.com",
                    password_hash="first-hash",
                )

            with pytest.raises(create_admin.DuplicateAdminEmailError), session.begin():
                create_admin.create_admin_account(
                    session,
                    full_name="Replacement Admin",
                    email="admin@example.com",
                    password_hash="replacement-hash",
                )

            existing_user = session.execute(
                text("SELECT full_name, password_hash, role, status FROM users")
            ).one()

        assert existing_user == ("First Admin", "first-hash", "ADMIN", "ACTIVE")
    finally:
        engine.dispose()


def test_inspect_database_target_checks_configured_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Đọc tên database/schema trả về để không xác nhận nhầm schema đang hoạt động."""

    session = MagicMock()
    session.execute.return_value.one.return_value = ("study_test", "study_test")
    engine = Mock()

    session.__enter__.return_value = session
    session.begin.return_value.__enter__.return_value = None
    monkeypatch.setattr(create_admin, "Session", lambda _engine: session)

    assert create_admin.inspect_database_target(engine, "study_test") == (
        "study_test",
        "study_test",
    )


def test_inspect_database_target_rejects_missing_configured_schema(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không cho xác nhận target nếu PostgreSQL đang dùng schema khác cấu hình."""

    session = MagicMock()
    session.__enter__.return_value = session
    session.begin.return_value.__enter__.return_value = None
    session.execute.return_value.one.return_value = ("study_test", "public")
    monkeypatch.setattr(create_admin, "Session", lambda _engine: session)

    with pytest.raises(create_admin.AdminBootstrapError, match="Schema"):
        create_admin.inspect_database_target(Mock(), "study_test")
