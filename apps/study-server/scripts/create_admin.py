"""Tạo tài khoản Admin Study Server bằng cấu hình database tường minh và prompt tương tác."""

# ruff: noqa: E402

from __future__ import annotations

import argparse
import getpass
import os
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path

# Thêm thư mục project vào import path để script chạy trực tiếp từ mọi working directory.
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Các import app phải theo sau khi thêm root vì script hỗ trợ chạy trực tiếp bằng đường dẫn.
# isort: off
from sqlalchemy import Engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.core.database import build_engine
from app.core.security.password import hash_password
from app.utils.validate import normalize_email
# isort: on

CHECK_EMAIL = text("SELECT id FROM users WHERE email = :email")
INSERT_ADMIN = text(
    """
    INSERT INTO users (
        full_name,
        email,
        password_hash,
        role,
        avatar_url,
        phone,
        status,
        created_at,
        updated_at
    )
    VALUES (
        :full_name,
        :email,
        :password_hash,
        'ADMIN',
        NULL,
        NULL,
        'ACTIVE',
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP
    )
    RETURNING id
    """
)


class AdminBootstrapError(Exception):
    """Đại diện lỗi cấu hình hoặc dữ liệu đầu vào có thể báo an toàn cho operator."""


class DuplicateAdminEmailError(AdminBootstrapError):
    """Báo email đã thuộc một tài khoản hiện có mà không sửa tài khoản đó."""


def load_explicit_settings(environment: Mapping[str, str]) -> Settings:
    """Tạo Settings chỉ từ ba biến STUDY_ADMIN bắt buộc, không dùng DB mặc định của ứng dụng."""

    required_names = (
        "STUDY_ADMIN_DATABASE_URL",
        "STUDY_ADMIN_DB_SCHEMA",
        "STUDY_ADMIN_APP_ENV",
    )
    missing_names = [name for name in required_names if not environment.get(name, "").strip()]
    if missing_names:
        raise AdminBootstrapError("Thiếu cấu hình bắt buộc: " + ", ".join(missing_names) + ".")

    database_url = environment["STUDY_ADMIN_DATABASE_URL"].strip()
    try:
        parsed_url = make_url(database_url)
    except Exception:
        raise AdminBootstrapError("STUDY_ADMIN_DATABASE_URL không hợp lệ.") from None
    if parsed_url.drivername not in {"postgresql", "postgresql+psycopg"}:
        raise AdminBootstrapError("Database URL phải dùng PostgreSQL.")

    app_env = environment["STUDY_ADMIN_APP_ENV"].strip().lower()
    try:
        return Settings(
            app_env=app_env,
            database_url=database_url,
            db_schema=environment["STUDY_ADMIN_DB_SCHEMA"].strip(),
        )
    except RuntimeError:
        raise AdminBootstrapError("Cấu hình môi trường hoặc schema không hợp lệ.") from None


def ensure_environment_allowed(settings: Settings, allow_production: bool) -> None:
    """Chặn production trừ khi operator đã truyền cờ cho phép một cách tường minh."""

    if settings.app_env == "production" and not allow_production:
        raise AdminBootstrapError(
            "Môi trường production đang bị chặn; chỉ tiếp tục với --allow-production."
        )


def prepare_admin_account(
    full_name: str,
    email: str,
    password: str,
) -> tuple[str, str, str]:
    """Chuẩn hóa tên/email theo API đăng ký, kiểm tra password không rỗng và trả password hash."""

    normalized_name = full_name.strip()
    if not normalized_name:
        raise AdminBootstrapError("Họ tên không được để trống.")
    if len(normalized_name) > 150:
        raise AdminBootstrapError("Họ tên không được vượt quá 150 ký tự.")

    normalized_email = normalize_email(email, max_length=255)
    if not isinstance(normalized_email, str):
        raise AdminBootstrapError("Email không hợp lệ hoặc vượt quá 255 ký tự.")
    if not password.strip():
        raise AdminBootstrapError("Mật khẩu không được để trống.")

    return normalized_name, normalized_email, hash_password(password)


def create_admin_account(
    session: Session,
    *,
    full_name: str,
    email: str,
    password_hash: str,
) -> int:
    """Từ chối email trùng rồi insert Admin bằng bind parameters; transaction thuộc caller."""

    existing_user_id = session.execute(CHECK_EMAIL, {"email": email}).scalar_one_or_none()
    if existing_user_id is not None:
        raise DuplicateAdminEmailError("Email đã tồn tại; không thay đổi tài khoản hiện có.")

    inserted_user_id = session.execute(
        INSERT_ADMIN,
        {
            "full_name": full_name,
            "email": email,
            "password_hash": password_hash,
        },
    ).scalar_one()
    return int(inserted_user_id)


def inspect_database_target(engine: Engine, expected_schema: str) -> tuple[str, str]:
    """Đọc tên database/schema thực tế qua transaction để kiểm tra đích trước khi tạo user."""

    with Session(engine) as session, session.begin():
        target = session.execute(text("SELECT current_database(), current_schema()")).one()
    database_name, schema_name = target
    if not database_name or schema_name != expected_schema:
        raise AdminBootstrapError(
            "Schema được cấu hình không tồn tại hoặc không phải schema đang hoạt động."
        )
    return str(database_name), str(schema_name)


def confirm_target(
    settings: Settings,
    engine: Engine,
    database_name: str,
    schema_name: str,
) -> bool:
    """Hiển thị đích không chứa credential và yêu cầu xác nhận chính xác trước mọi ghi dữ liệu."""

    url = engine.url
    host = url.host or "(unknown host)"
    port = f":{url.port}" if url.port is not None else ""
    phrase = "CREATE ADMIN IN PRODUCTION" if settings.app_env == "production" else "CREATE ADMIN"
    print(
        "Đích database: "
        f"env={settings.app_env}, host={host}{port}, "
        f"database={database_name}, schema={schema_name}"
    )
    if settings.app_env == "production":
        print("Đây là thao tác tạo tài khoản có quyền quản trị production.")
    return input(f"Nhập chính xác '{phrase}' để tiếp tục: ").strip() == phrase


def prompt_admin_details() -> tuple[str, str, str]:
    """Nhập tên/email và password ẩn hai lần; không nhận credential qua command arguments."""

    full_name = input("Họ tên Admin: ")
    email = input("Email Admin: ")
    password = getpass.getpass("Mật khẩu Admin: ")
    password_confirmation = getpass.getpass("Nhập lại mật khẩu: ")
    if password != password_confirmation:
        raise AdminBootstrapError("Hai lần nhập mật khẩu không khớp.")
    return full_name, email, password


def build_argument_parser() -> argparse.ArgumentParser:
    """Tạo parser CLI với cờ riêng để cho phép bootstrap trong production."""

    parser = argparse.ArgumentParser(description="Tạo một tài khoản Admin cho Study Server.")
    parser.add_argument(
        "--allow-production",
        action="store_true",
        help="Cho phép nhắm production; vẫn cần xác nhận bằng cụm từ riêng.",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    """Chạy flow kiểm tra target, xác nhận, nhập dữ liệu, insert transaction và đóng engine."""

    parsed_arguments = build_argument_parser().parse_args(arguments)
    try:
        settings = load_explicit_settings(os.environ)
        ensure_environment_allowed(settings, parsed_arguments.allow_production)
    except AdminBootstrapError as exc:
        print(f"Không thể tạo Admin: {exc}", file=sys.stderr)
        return 2

    engine: Engine | None = None
    try:
        engine = build_engine(settings)
        database_name, schema_name = inspect_database_target(engine, settings.db_schema)
        if not confirm_target(settings, engine, database_name, schema_name):
            print("Đã hủy; không có thay đổi nào được ghi.")
            return 0

        full_name, email, password = prompt_admin_details()
        normalized_name, normalized_email, password_hash = prepare_admin_account(
            full_name,
            email,
            password,
        )
        with Session(engine) as session, session.begin():
            user_id = create_admin_account(
                session,
                full_name=normalized_name,
                email=normalized_email,
                password_hash=password_hash,
            )
    except DuplicateAdminEmailError as exc:
        print(f"Không thể tạo Admin: {exc}", file=sys.stderr)
        return 1
    except AdminBootstrapError as exc:
        print(f"Không thể tạo Admin: {exc}", file=sys.stderr)
        return 1
    except IntegrityError:
        print(
            "Database từ chối insert do ràng buộc dữ liệu; transaction đã rollback.",
            file=sys.stderr,
        )
        return 1
    except SQLAlchemyError:
        print("Không thể hoàn thành thao tác database; transaction đã rollback.", file=sys.stderr)
        return 1
    except (EOFError, KeyboardInterrupt):
        print("Đã hủy; không có thay đổi nào được ghi.", file=sys.stderr)
        return 130
    finally:
        if engine is not None:
            engine.dispose()

    print(f"Đã tạo Admin: id={user_id}, email={normalized_email}, role=ADMIN, status=ACTIVE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
