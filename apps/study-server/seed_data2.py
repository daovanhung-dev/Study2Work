"""Tạo dữ liệu mẫu để kiểm tra API #32 bằng cấu hình database của dự án.

Mặc định script chạy dry-run và rollback. Chỉ thêm --apply sau khi xác nhận
đúng database đích để commit dữ liệu. Script tạo hoặc dùng lại tài khoản test và không xóa dữ liệu.
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import get_engine
from app.core.security import hash_password, verify_password


def ensure_student(connection, *, email: str, password: str, now: datetime) -> int:
    """Tạo Student test ACTIVE hoặc xác nhận tài khoản test đã có thể dùng."""
    row = (
        connection.execute(
            text("""
                SELECT id, password_hash, role, status
                FROM users
                WHERE email = :email
                LIMIT 1
            """),
            {"email": email},
        )
        .mappings()
        .first()
    )

    if row is not None:
        if str(row["role"]).upper() != "STUDENT":
            raise ValueError(
                f"Email {email} đã tồn tại nhưng không có role STUDENT; "
                "script không tự đổi role."
            )
        if str(row["status"]).upper() != "ACTIVE":
            raise ValueError(
                f"Student {email} chưa ACTIVE; script không tự kích hoạt tài khoản."
            )
        if not verify_password(password, str(row["password_hash"])):
            raise ValueError(
                f"Student {email} đã tồn tại nhưng mật khẩu khác mật khẩu test. "
                "Hãy chọn API32_STUDENT_EMAIL khác; script không đổi mật khẩu cũ."
            )
        print(f"Dùng lại Student test: {email}")
        return int(row["id"])

    row = (
        connection.execute(
            text("""
                INSERT INTO users (
                    email,
                    password_hash,
                    full_name,
                    role,
                    status,
                    created_at,
                    updated_at
                )
                VALUES (
                    :email,
                    :password_hash,
                    'API 32 Test Student',
                    'STUDENT',
                    'ACTIVE',
                    :now,
                    :now
                )
                RETURNING id
            """),
            {
                "email": email,
                "password_hash": hash_password(password),
                "now": now,
            },
        )
        .mappings()
        .one()
    )
    print(f"Đã tạo Student test ACTIVE: {email}")
    return int(row["id"])

def ensure_mentor(connection, *, email: str, password: str, now: datetime) -> int:
    """Tạo mentor test ACTIVE hoặc xác nhận tài khoản test đã có thể dùng."""
    row = (
        connection.execute(
            text("""
                SELECT id, password_hash, role, status
                FROM users
                WHERE email = :email
                LIMIT 1
            """),
            {"email": email},
        )
        .mappings()
        .first()
    )
    if row is not None:
        if str(row["role"]).upper() != "MENTOR":
            raise ValueError(f"Email {email} đã tồn tại nhưng không có role MENTOR.")
        if str(row["status"]).upper() != "ACTIVE":
            raise ValueError(f"Mentor {email} chưa ACTIVE.")
        if not verify_password(password, str(row["password_hash"])):
            raise ValueError(
                f"Mentor {email} đã tồn tại với mật khẩu khác; "
                "hãy chọn API32_MENTOR_EMAIL khác."
            )
        return int(row["id"])

    row = (
        connection.execute(
            text("""
                INSERT INTO users (
                    email, password_hash, full_name, role, status,
                    created_at, updated_at
                )
                VALUES (
                    :email, :password_hash, 'API 32 Test Mentor',
                    'MENTOR', 'ACTIVE', :now, :now
                )
                RETURNING id
            """),
            {
                "email": email,
                "password_hash": hash_password(password),
                "now": now,
            },
        )
        .mappings()
        .one()
    )
    print(f"Đã tạo Mentor test ACTIVE: {email}")
    return int(row["id"])


def get_or_create_course(connection, mentor_id: int, now: datetime) -> int:
    """Tạo hoặc lấy khóa học riêng cho fixture API #32."""
    name = "SEED_API32_ATTEMPTS_RESULT_COURSE"
    row = (
        connection.execute(
            text("""
                SELECT id
                FROM courses
                WHERE mentor_id = :mentor_id AND name = :name
                ORDER BY id
                LIMIT 1
            """),
            {"mentor_id": mentor_id, "name": name},
        )
        .mappings()
        .first()
    )
    if row is not None:
        return int(row["id"])

    row = (
        connection.execute(
            text("""
                INSERT INTO courses (
                    mentor_id, name, description, price, status,
                    created_at, updated_at
                )
                VALUES (
                    :mentor_id, :name, 'Dữ liệu test API #32',
                    0, 'PUBLISHED', :now, :now
                )
                RETURNING id
            """),
            {"mentor_id": mentor_id, "name": name, "now": now},
        )
        .mappings()
        .one()
    )
    return int(row["id"])


def get_or_create_quiz(
    connection, *, course_id: int, student_id: int, now: datetime
) -> int:
    """Tạo hoặc lấy quiz riêng cho student đang được seed."""
    name = f"SEED_API32_ATTEMPTS_RESULT_{student_id}"
    row = (
        connection.execute(
            text("""
                SELECT id
                FROM quizzes
                WHERE name = :name AND course_id = :course_id
                ORDER BY id
                LIMIT 1
            """),
            {"name": name, "course_id": course_id},
        )
        .mappings()
        .first()
    )
    if row is not None:
        return int(row["id"])

    row = (
        connection.execute(
            text("""
                INSERT INTO quizzes (
                    course_id, name, description, passing_score,
                    time_limit_minutes, status, created_at, updated_at
                )
                VALUES (
                    :course_id, :name, 'Dữ liệu test API #32',
                    0, NULL, 'PUBLISHED', :now, :now
                )
                RETURNING id
            """),
            {"course_id": course_id, "name": name, "now": now},
        )
        .mappings()
        .one()
    )
    return int(row["id"])


def get_or_create_question(
    connection, quiz_id: int, student_id: int
) -> tuple[int, int]:
    """Tạo hoặc lấy câu hỏi và choice mẫu; trả về cả hai ID."""
    question_text = f"SEED_API32_QUESTION_{student_id}"
    row = (
        connection.execute(
            text("""
                SELECT id
                FROM quiz_questions
                WHERE quiz_id = :quiz_id AND question_text = :question_text
                ORDER BY id
                LIMIT 1
            """),
            {"quiz_id": quiz_id, "question_text": question_text},
        )
        .mappings()
        .first()
    )
    if row is None:
        row = (
            connection.execute(
                text("""
                    INSERT INTO quiz_questions (
                        quiz_id, question_text, sort_order, score
                    )
                    VALUES (:quiz_id, :question_text, 1, 10.00)
                    RETURNING id
                """),
                {"quiz_id": quiz_id, "question_text": question_text},
            )
            .mappings()
            .one()
        )

    question_id = int(row["id"])
    choice_text = f"SEED_API32_CHOICE_{student_id}"
    choice = (
        connection.execute(
            text("""
                SELECT id
                FROM quiz_choices
                WHERE question_id = :question_id AND choice_text = :choice_text
                ORDER BY id
                LIMIT 1
            """),
            {"question_id": question_id, "choice_text": choice_text},
        )
        .mappings()
        .first()
    )
    if choice is None:
        choice = (
            connection.execute(
                text("""
                    INSERT INTO quiz_choices (question_id, choice_text, is_correct)
                    VALUES (:question_id, :choice_text, TRUE)
                    RETURNING id
                """),
                {"question_id": question_id, "choice_text": choice_text},
            )
            .mappings()
            .one()
        )
    return question_id, int(choice["id"])

def get_or_create_attempt(
    connection,
    *,
    quiz_id: int,
    student_id: int,
    status: str,
    started_at: datetime,
    submitted_at: datetime,
    score: Decimal | None,
) -> int:
    """Tạo attempt theo trạng thái hoặc cập nhật lại fixture đã seed trước đó."""
    row = (
        connection.execute(
            text("""
                SELECT id
                FROM quiz_attempts
                WHERE quiz_id = :quiz_id
                  AND user_id = :student_id
                  AND status = :status
                ORDER BY id
                LIMIT 1
            """),
            {
                "quiz_id": quiz_id,
                "student_id": student_id,
                "status": status,
            },
        )
        .mappings()
        .first()
    )

    params = {
        "quiz_id": quiz_id,
        "student_id": student_id,
        "status": status,
        "started_at": started_at,
        "submitted_at": submitted_at,
        "score": score,
    }

    if row is not None:
        attempt_id = int(row["id"])
        connection.execute(
            text("""
                UPDATE quiz_attempts
                SET started_at = :started_at,
                    submitted_at = :submitted_at,
                    score = :score,
                    status = :status
                WHERE id = :attempt_id
            """),
            {**params, "attempt_id": attempt_id},
        )
        return attempt_id

    row = (
        connection.execute(
            text("""
                INSERT INTO quiz_attempts (
                    quiz_id,
                    user_id,
                    started_at,
                    submitted_at,
                    score,
                    status
                )
                VALUES (
                    :quiz_id,
                    :student_id,
                    :started_at,
                    :submitted_at,
                    :score,
                    :status
                )
                RETURNING id
            """),
            params,
        )
        .mappings()
        .one()
    )
    return int(row["id"])


def get_or_create_answer(
    connection,
    *,
    attempt_id: int,
    question_id: int,
    choice_id: int,
    is_correct: bool,
    score_received: Decimal,
) -> None:
    """Tạo hoặc cập nhật câu trả lời mẫu theo các cột của DB design."""
    row = (
        connection.execute(
            text("""
                SELECT id
                FROM quiz_answers
                WHERE attempt_id = :attempt_id AND question_id = :question_id
                ORDER BY id
                LIMIT 1
            """),
            {"attempt_id": attempt_id, "question_id": question_id},
        )
        .mappings()
        .first()
    )
    params = {
        "attempt_id": attempt_id,
        "question_id": question_id,
        "choice_id": choice_id,
        "is_correct": is_correct,
        "score_received": score_received,
    }
    if row is not None:
        connection.execute(
            text("""
                UPDATE quiz_answers
                SET choice_id = :choice_id,
                    is_correct = :is_correct,
                    score_received = :score_received
                WHERE id = :answer_id
            """),
            {**params, "answer_id": int(row["id"])},
        )
        return

    connection.execute(
        text("""
            INSERT INTO quiz_answers (
                attempt_id, question_id, choice_id, is_correct, score_received
            )
            VALUES (
                :attempt_id, :question_id, :choice_id, :is_correct, :score_received
            )
        """),
        params,
    )

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Tạo dữ liệu test cho API #32 attempts_result."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Commit dữ liệu. Cần gõ COMMIT sau khi xác nhận database đích.",
    )
    args = parser.parse_args()

    student_email = os.getenv(
        "API32_STUDENT_EMAIL", "api32.student@example.com"
    ).strip()
    student_password = os.getenv(
        "API32_STUDENT_PASSWORD", "Study2Work-API32-Test-2026!"
    ).strip()
    mentor_email = os.getenv(
        "API32_MENTOR_EMAIL", "api32.mentor@example.com"
    ).strip()
    mentor_password = os.getenv(
        "API32_MENTOR_PASSWORD", "Study2Work-API32-Mentor-2026!"
    ).strip()
    if any(not value or "<" in value or ">" in value for value in (student_email, mentor_email)):
        print("API32_STUDENT_EMAIL/API32_MENTOR_EMAIL không hợp lệ.", file=sys.stderr)
        return 2
    if len(student_password) < 8 or len(mentor_password) < 8:
        print("Mật khẩu test phải có ít nhất 8 ký tự.", file=sys.stderr)
        return 2

    try:
        settings = get_settings()
        engine = get_engine()
    except (ValueError, SQLAlchemyError):
        print(
            "Không thể nạp cấu hình database của dự án. Kiểm tra cấu hình hiện tại.",
            file=sys.stderr,
        )
        return 1

    host = engine.url.host or "(không rõ host)"
    database = engine.url.database or "(không rõ database)"
    schema = settings.db_schema
    print(f"Database đích: host={host}; database={database}; schema={schema}")

    if args.apply:
        confirmation = input(
            f"Gõ COMMIT để ghi dữ liệu vào {database} trên {host} (schema {schema}): "
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
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        student_id = ensure_student(
            connection,
            email=student_email,
            password=student_password,
            now=now,
        )
        mentor_id = ensure_mentor(
            connection,
            email=mentor_email,
            password=mentor_password,
            now=now,
        )
        course_id = get_or_create_course(connection, mentor_id, now)
        quiz_id = get_or_create_quiz(
            connection, course_id=course_id, student_id=student_id, now=now
        )
        question_id, choice_id = get_or_create_question(
            connection, quiz_id, student_id
        )

        graded_attempt_id = get_or_create_attempt(
            connection,
            quiz_id=quiz_id,
            student_id=student_id,
            status="GRADED",
            started_at=now - timedelta(hours=2),
            submitted_at=now - timedelta(hours=1),
            score=Decimal("8.50"),
        )
        get_or_create_answer(
            connection,
            attempt_id=graded_attempt_id,
            question_id=question_id,
            choice_id=choice_id,
            is_correct=True,
            score_received=Decimal("8.50"),
        )

        pending_attempt_id = get_or_create_attempt(
            connection,
            quiz_id=quiz_id,
            student_id=student_id,
            status="PENDING_GRADE",
            started_at=now - timedelta(minutes=45),
            submitted_at=now - timedelta(minutes=30),
            score=None,
        )
        get_or_create_answer(
            connection,
            attempt_id=pending_attempt_id,
            question_id=question_id,
            choice_id=choice_id,
            is_correct=False,
            score_received=Decimal("0.00"),
        )

        if args.apply:
            transaction.commit()
            print("\nĐã commit dữ liệu.")
        else:
            transaction.rollback()
            print("\nDry run: đã rollback, không lưu row mới hoặc cập nhật nào.")
            print("Các ID dưới đây chỉ dùng được sau khi chạy lại với --apply.")

        print("\n========== THÔNG TIN TEST API #32 ==========")
        print(f"Student email      : {student_email}")
        print(f"Student password   : {student_password}")
        print(f"Student ID         : {student_id}")
        print(f"Course ID          : {course_id}")
        print(f"Quiz ID            : {quiz_id}")
        print(f"Question ID        : {question_id}")
        print(f"GRADED attempt ID  : {graded_attempt_id}")
        print(f"PENDING attempt ID : {pending_attempt_id}")
        print(f"GET URL            : /api/v1/attempts/{graded_attempt_id}/result")
        print(f"GET URL            : /api/v1/attempts/{pending_attempt_id}/result")
        if not args.apply:
            print("\nNếu database đích đúng, chạy lại lệnh với --apply để lưu dữ liệu.")
        return 0
    except (SQLAlchemyError, ValueError) as exc:
        if transaction is not None and transaction.is_active:
            transaction.rollback()
        print(f"\nKhông thể seed dữ liệu: {exc}", file=sys.stderr)
        return 1
    finally:
        if connection is not None:
            connection.close()
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
