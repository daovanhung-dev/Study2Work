from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import uuid4

from sqlalchemy import MetaData, Table, inspect, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import get_engine
from app.core.security import hash_password, verify_password


STUDENT_EMAIL = "api33.student@example.com"
STUDENT_PASSWORD = "Study2Work-Test-2026!"

MENTOR_EMAIL = "api33.mentor@example.com"
MENTOR_PASSWORD = "Api33-Mentor-Test-2026!"

COURSE_NAME = "API33 Test Course"
ASSIGNMENT_NAME = "API33 Test Assignment"


class SeedError(Exception):
    """Lỗi schema hoặc dữ liệu seed không đáp ứng yêu cầu."""


def utc_now_naive() -> datetime:
    """Sinh UTC timestamp không timezone cho cột TIMESTAMP trong ERD hiện tại."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_table(connection: Any, table_name: str) -> Table:
    """Đọc cấu trúc bảng từ database đang được cấu hình."""
    inspector = inspect(connection)
    if not inspector.has_table(table_name):
        raise SeedError(f"Không tìm thấy bảng {table_name!r} trong schema hiện hành.")

    return Table(table_name, MetaData(), autoload_with=connection)


def column_names(table: Table) -> set[str]:
    return {column.name for column in table.columns}


def is_uuid_type(column: Any) -> bool:
    return "UUID" in str(column.type).upper()


def has_database_generated_value(column: Any) -> bool:
    """Nhận diện ID/default do database tạo để không tự bịa giá trị."""
    return (
        column.default is not None
        or column.server_default is not None
        or column.autoincrement is True
        or getattr(column, "identity", None) is not None
        or getattr(column, "computed", None) is not None
    )


def prepare_values(table: Table, supplied: dict[str, Any]) -> dict[str, Any]:
    """Giữ các giá trị có cột tương ứng và báo lỗi nếu thiếu cột bắt buộc."""
    values = {key: value for key, value in supplied.items() if key in table.c}

    for column in table.columns:
        if column.name in values or has_database_generated_value(column) or column.nullable:
            continue

        if column.primary_key and is_uuid_type(column):
            values[column.name] = uuid4()
            continue

        if column.primary_key:
            raise SeedError(
                f"Không biết cách tạo khóa chính {table.name}.{column.name}; "
                "hãy kiểm tra schema trước."
            )

        raise SeedError(
            f"Thiếu giá trị cho cột bắt buộc {table.name}.{column.name}; "
            "script dừng để không đoán dữ liệu."
        )

    return values


def insert_row(connection: Any, table: Table, supplied: dict[str, Any]) -> dict[str, Any]:
    """Insert row và lấy lại các giá trị do database tạo."""
    values = prepare_values(table, supplied)
    result = connection.execute(
        table.insert().values(**values).returning(*table.columns)
    )
    row = result.fetchone()
    if row is None:
        raise SeedError(f"Database không trả về row vừa insert vào {table.name}.")
    return dict(row._mapping)


def find_by_email(connection: Any, users: Table, email: str) -> dict[str, Any] | None:
    if "email" not in users.c:
        raise SeedError("Bảng users không có cột email.")
    row = connection.execute(
        select(users).where(users.c.email == email).limit(1)
    ).first()
    return dict(row._mapping) if row is not None else None


def ensure_user(
    connection: Any,
    *,
    email: str,
    password: str,
    full_name: str,
    role: str,
    verify_existing_password: bool,
) -> dict[str, Any]:
    """Tạo test user nếu chưa có; không âm thầm đổi mật khẩu user cũ."""
    users = get_table(connection, "users")
    existing = find_by_email(connection, users, email)

    if existing is not None:
        if str(existing.get("role", "")).upper() != role:
            raise SeedError(
                f"Tài khoản {email} đã tồn tại nhưng role không phải {role}; "
                "script không tự đổi role."
            )
        if str(existing.get("status", "")).upper() != "ACTIVE":
            raise SeedError(
                f"Tài khoản {email} đã tồn tại nhưng không ACTIVE; "
                "script không tự bật tài khoản."
            )
        if verify_existing_password and not verify_password(
            password,
            str(existing.get("password_hash", "")),
        ):
            raise SeedError(
                f"Tài khoản {email} đã tồn tại với password khác. "
                "Hãy dùng tài khoản test khác hoặc xử lý thủ công trong DB dev."
            )
        print(f"Dùng lại tài khoản {role}: {email}")
        return existing

    now = utc_now_naive()
    user = insert_row(
        connection,
        users,
        {
            "email": email,
            "password_hash": hash_password(password),
            "full_name": full_name,
            "role": role,
            "status": "ACTIVE",
            "created_at": now,
            "updated_at": now,
        },
    )
    print(f"Đã tạo tài khoản {role}: {email}")
    return user


def ensure_course(connection: Any, mentor: dict[str, Any]) -> dict[str, Any]:
    """Tìm hoặc tạo course test gắn với mentor test, không lấy course bất kỳ."""
    courses = get_table(connection, "courses")
    required = {"id", "mentor_id", "name"}
    missing = required - column_names(courses)
    if missing:
        raise SeedError(
            "Bảng courses thiếu cột cần dùng: " + ", ".join(sorted(missing))
        )

    mentor_id = mentor.get("id")
    if mentor_id is None:
        raise SeedError("Không lấy được users.id của mentor test.")

    row = connection.execute(
        select(courses)
        .where(courses.c.mentor_id == mentor_id, courses.c.name == COURSE_NAME)
        .limit(1)
    ).first()
    if row is not None:
        course = dict(row._mapping)
        print(f"Dùng lại course test: id={course.get('id')}")
        return course

    now = utc_now_naive()
    course = insert_row(
        connection,
        courses,
        {
            "mentor_id": mentor_id,
            "name": COURSE_NAME,
            "description": "Course mẫu để kiểm thử API #33.",
            "price": Decimal("0.00"),
            "status": "PUBLISHED",
            "created_at": now,
            "updated_at": now,
        },
    )
    print(f"Đã tạo course test: id={course.get('id')}")
    return course


def ensure_assignment(connection: Any, course: dict[str, Any]) -> dict[str, Any]:
    """Tìm hoặc tạo assignment test riêng trong course test."""
    assignments = get_table(connection, "assignments")
    required = {
        "id",
        "course_id",
        "name",
        "description",
        "due_at",
        "max_score",
    }
    missing = required - column_names(assignments)
    if missing:
        raise SeedError(
            "Bảng assignments thiếu cột API #33 cần đọc: "
            + ", ".join(sorted(missing))
        )

    course_id = course.get("id")
    if course_id is None:
        raise SeedError("Không lấy được courses.id của course test.")

    row = connection.execute(
        select(assignments)
        .where(
            assignments.c.course_id == course_id,
            assignments.c.name == ASSIGNMENT_NAME,
        )
        .limit(1)
    ).first()
    if row is not None:
        assignment = dict(row._mapping)
        print(f"Dùng lại assignment test: id={assignment.get('id')}")
        return assignment

    now = utc_now_naive()
    assignment = insert_row(
        connection,
        assignments,
        {
            "course_id": course_id,
            "name": ASSIGNMENT_NAME,
            "description": "Assignment mẫu để kiểm thử GET /api/v1/assignments/{assignment_id}.",
            "due_at": now.replace(microsecond=0),
            "max_score": Decimal("100.00"),
            "created_at": now,
            "updated_at": now,
        },
    )
    print(f"Đã tạo assignment test: id={assignment.get('id')}")
    return assignment


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tạo dữ liệu test cô lập cho API #33."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit dữ liệu. Cần gõ COMMIT sau khi xác nhận database đích.",
    )
    args = parser.parse_args()

    engine = get_engine()
    host = engine.url.host or "(không rõ host)"
    database = engine.url.database or "(không rõ database)"
    print(f"Database đích: host={host}; database={database}")

    if args.apply:
        confirmation = input(
            f"Gõ COMMIT để ghi dữ liệu vào {database} trên {host}: "
        ).strip()
        if confirmation != "COMMIT":
            print("Đã hủy, không ghi dữ liệu.")
            engine.dispose()
            return 2

    connection = None
    transaction = None
    try:
        connection = engine.connect()
        transaction = connection.begin()

        ensure_user(
            connection,
            email=STUDENT_EMAIL,
            password=STUDENT_PASSWORD,
            full_name="API33 Test Student",
            role="STUDENT",
            verify_existing_password=True,
        )
        mentor = ensure_user(
            connection,
            email=MENTOR_EMAIL,
            password=MENTOR_PASSWORD,
            full_name="API33 Test Mentor",
            role="MENTOR",
            verify_existing_password=False,
        )
        course = ensure_course(connection, mentor)
        assignment = ensure_assignment(connection, course)

        assignment_id = assignment.get("id")
        if args.apply:
            transaction.commit()
            print("\\nĐã commit dữ liệu.")
        else:
            transaction.rollback()
            print("\\nDry run: đã rollback, không lưu row mới.")
            print("ID của row mới ở chế độ này không dùng để gọi API.")

        print("\\n========== THÔNG TIN TEST API #33 ==========")
        print(f"Student email : {STUDENT_EMAIL}")
        print(f"Student pass  : {STUDENT_PASSWORD}")
        print(f"Course ID     : {course.get('id')}")
        print(f"Assignment ID : {assignment_id}")
        print(f"GET URL       : /api/v1/assignments/{assignment_id}")
        if not args.apply:
            print("\\nSau khi xác minh đúng DB dev/test, chạy lại với --apply.")

        return 0
    except (SeedError, SQLAlchemyError, ValueError) as exc:
        if transaction is not None and transaction.is_active:
            transaction.rollback()
        print(f"\\nKhông thể seed dữ liệu: {exc}", file=sys.stderr)
        return 1
    finally:
        if connection is not None:
            connection.close()
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())

