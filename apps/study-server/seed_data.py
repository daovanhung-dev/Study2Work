from datetime import datetime

from sqlalchemy import text

from app.core.database import get_engine


def get_or_create_user(connection, email, full_name, role):
    """Lấy user theo email hoặc tạo mới user phục vụ test API #10."""
    row = connection.execute(
        text("""
            INSERT INTO users (
                full_name,
                email,
                password_hash,
                role,
                status,
                created_at,
                updated_at
            )
            VALUES (
                :full_name,
                :email,
                :password_hash,
                :role,
                'ACTIVE',
                :now,
                :now
            )
            ON CONFLICT (email)
            DO UPDATE SET full_name = EXCLUDED.full_name
            RETURNING id
        """),
        {
            "full_name": full_name,
            "email": email,
            "password_hash": "seed-only-not-a-real-password-hash",
            "role": role,
            "now": datetime.now(),
        },
    ).mappings().one()

    return int(row["id"])


def get_or_create_course(connection, mentor_id, name, status):
    """Lấy khóa học seed đã có hoặc tạo mới khóa học theo trạng thái."""
    row = connection.execute(
        text("""
            SELECT id
            FROM courses
            WHERE mentor_id = :mentor_id
              AND name = :name
              AND status = :status
            ORDER BY id
            LIMIT 1
        """),
        {
            "mentor_id": mentor_id,
            "name": name,
            "status": status,
        },
    ).mappings().first()

    if row is not None:
        return int(row["id"])

    row = connection.execute(
        text("""
            INSERT INTO courses (
                mentor_id,
                name,
                description,
                price,
                status,
                created_at,
                updated_at
            )
            VALUES (
                :mentor_id,
                :name,
                :description,
                0,
                :status,
                :now,
                :now
            )
            RETURNING id
        """),
        {
            "mentor_id": mentor_id,
            "name": name,
            "description": "Du lieu seed de test API #10",
            "status": status,
            "now": datetime.now(),
        },
    ).mappings().one()

    return int(row["id"])


def get_or_create_discussion(
    connection,
    course_id,
    user_id,
    parent_id,
    content,
):
    """Lấy review/reply đã có hoặc tạo mới để tránh chèn trùng khi chạy lại."""
    row = connection.execute(
        text("""
            SELECT id
            FROM discussions
            WHERE course_id = :course_id
              AND user_id = :user_id
              AND content = :content
              AND parent_id IS NOT DISTINCT FROM :parent_id
            ORDER BY id
            LIMIT 1
        """),
        {
            "course_id": course_id,
            "user_id": user_id,
            "parent_id": parent_id,
            "content": content,
        },
    ).mappings().first()

    if row is not None:
        return int(row["id"])

    row = connection.execute(
        text("""
            INSERT INTO discussions (
                course_id,
                user_id,
                parent_id,
                content,
                status,
                created_at,
                updated_at
            )
            VALUES (
                :course_id,
                :user_id,
                :parent_id,
                :content,
                'ACTIVE',
                :now,
                :now
            )
            RETURNING id
        """),
        {
            "course_id": course_id,
            "user_id": user_id,
            "parent_id": parent_id,
            "content": content,
            "now": datetime.now(),
        },
    ).mappings().one()

    return int(row["id"])


def main():
    """Tạo dữ liệu thử nghiệm cho API #10 trong một transaction."""
    engine = get_engine()

    with engine.begin() as connection:
        mentor_id = get_or_create_user(
            connection,
            "seed_api10_mentor@example.test",
            "API10 Test Mentor",
            "MENTOR",
        )
        student_a_id = get_or_create_user(
            connection,
            "seed_api10_student_a@example.test",
            "API10 Test Student A",
            "STUDENT",
        )
        student_b_id = get_or_create_user(
            connection,
            "seed_api10_student_b@example.test",
            "API10 Test Student B",
            "STUDENT",
        )

        # Khóa học có review để test thành công và phân trang.
        published_course_id = get_or_create_course(
            connection,
            mentor_id,
            "SEED API10 - Published Reviews",
            "PUBLISHED",
        )

        # Khóa học không có review để test danh sách rỗng.
        empty_course_id = get_or_create_course(
            connection,
            mentor_id,
            "SEED API10 - Empty Reviews",
            "PUBLISHED",
        )

        # Khóa học chưa publish để test phản hồi 404.
        draft_course_id = get_or_create_course(
            connection,
            mentor_id,
            "SEED API10 - Draft Reviews",
            "DRAFT",
        )

        first_review_id = None

        # Tạo 21 review gốc để có dữ liệu cho trang 1 và trang 2.
        for index in range(1, 22):
            reviewer_id = (
                student_a_id if index % 2 == 1 else student_b_id
            )
            review_id = get_or_create_discussion(
                connection,
                published_course_id,
                reviewer_id,
                None,
                f"SEED_API10_REVIEW_{index:02d}",
            )

            if index == 1:
                first_review_id = review_id

        # Tạo một reply cho review đầu tiên.
        get_or_create_discussion(
            connection,
            published_course_id,
            mentor_id,
            first_review_id,
            "SEED_API10_REPLY_01",
        )

    print("Seed API #10 hoàn tất.")
    print(f"Course có review (PUBLISHED): {published_course_id}")
    print(f"Course rỗng (PUBLISHED):      {empty_course_id}")
    print(f"Course chưa publish (DRAFT):  {draft_course_id}")
    print("Course có review: 21 review gốc và 1 reply.")
    print("Hãy dùng các course_id ở trên để test Thunder Client.")


if __name__ == "__main__":
    main()