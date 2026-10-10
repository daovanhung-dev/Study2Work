"""Script nạp seed data cho API #11 và API #15 trên Study Server.

Sử dụng cấu hình Settings hiện hành (schema hoang_xuan_long trên Neon PostgreSQL).
Đồng thời tạo sẵn JWT token cho học viên để test API #15 qua Thunder Client.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Đảm bảo đường dẫn import app
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Đảm bảo stdout hiển thị tiếng Việt trên Windows console
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

from sqlalchemy import text
from app.core.config import get_settings
from app.core.database import get_engine
from app.core.security.access_token import create_access_token


def seed_database() -> None:
    """Nạp dữ liệu mẫu vào schema được cấu hình."""
    settings = get_settings()
    schema = settings.DB_SCHEMA
    print(f"[*] Đang kết nối CSDL và áp dụng seed data vào schema: '{schema}'...")

    engine = get_engine()

    sql_statements = [
        f"SET search_path TO {schema}, public",
        """
        INSERT INTO users (id, full_name, email, password_hash, role, avatar_url, phone, status, created_at, updated_at)
        VALUES 
            (1, 'Nguyen Van Mentor', 'mentor@study2work.edu.vn', '$2b$12$e8Y5t1examplehashmentor', 'MENTOR', 'https://cdn.example.com/avatars/mentor.png', '0901234567', 'ACTIVE', NOW(), NOW()),
            (2, 'Tran Thi Student', 'student@study2work.edu.vn', '$2b$12$e8Y5t1examplehashstudent', 'STUDENT', 'https://cdn.example.com/avatars/student.png', '0907654321', 'ACTIVE', NOW(), NOW()),
            (3, 'Le Van Guest', 'guest@study2work.edu.vn', '$2b$12$e8Y5t1examplehashguest', 'STUDENT', 'https://cdn.example.com/avatars/guest.png', '0908889999', 'ACTIVE', NOW(), NOW())
        ON CONFLICT (id) DO UPDATE 
        SET full_name = EXCLUDED.full_name,
            email = EXCLUDED.email,
            role = EXCLUDED.role,
            status = EXCLUDED.status,
            updated_at = NOW()
        """,
        """
        INSERT INTO courses (id, mentor_id, name, description, thumbnail_url, price, status, created_at, updated_at)
        VALUES 
            (1, 1, 'Lập trình Backend FastAPI từ căn bản đến nâng cao', 'Khóa học làm chủ FastAPI, PostgreSQL và kiến trúc ứng dụng.', 'https://cdn.example.com/courses/fastapi-thumb.jpg', 599000.00, 'PUBLISHED', NOW(), NOW()),
            (2, 1, 'Lập trình Frontend Vue 3 căn bản', 'Khóa học nhập môn Vue 3 và Vite.', 'https://cdn.example.com/courses/vue-thumb.jpg', 399000.00, 'PUBLISHED', NOW(), NOW()),
            (3, 1, 'DevOps và CI/CD với Docker', 'Khóa học đang biên soạn.', 'https://cdn.example.com/courses/devops-thumb.jpg', 450000.00, 'DRAFT', NOW(), NOW())
        ON CONFLICT (id) DO UPDATE 
        SET mentor_id = EXCLUDED.mentor_id,
            name = EXCLUDED.name,
            description = EXCLUDED.description,
            status = EXCLUDED.status,
            updated_at = NOW()
        """,
        """
        INSERT INTO lessons (id, course_id, name, content, video_url, sort_order, status, created_at, updated_at)
        VALUES 
            (1, 1, 'Bài 1: Giới thiệu tổng quan hệ thống Study2Work', 'Nội dung giới thiệu kiến trúc client-server và API contract.', 'https://video.example.com/lessons/lesson_1.mp4', 1, 'PUBLISHED', NOW(), NOW()),
            (2, 1, 'Bài 2: Thiết kế Schema CSDL PostgreSQL', 'Nội dung về thiết kế bảng, khóa chính và foreign key.', 'https://video.example.com/lessons/lesson_2.mp4', 2, 'PUBLISHED', NOW(), NOW())
        ON CONFLICT (id) DO UPDATE 
        SET course_id = EXCLUDED.course_id,
            name = EXCLUDED.name,
            status = EXCLUDED.status,
            updated_at = NOW()
        """,
        """
        INSERT INTO resources (id, lesson_id, name, resource_type, url, created_at)
        VALUES 
            (1, 1, 'Tai_lieu_kien_truc_study2work.pdf', 'DOCUMENT', 'https://cdn.example.com/resources/Tai_lieu_kien_truc_study2work.pdf', NOW()),
            (2, 1, 'Source_code_mau_bai_1.zip', 'ARCHIVE', 'https://cdn.example.com/resources/Source_code_mau_bai_1.zip', NOW()),
            (3, 2, 'Slide_thiet_ke_database.pdf', 'DOCUMENT', 'https://cdn.example.com/resources/Slide_thiet_ke_database.pdf', NOW())
        ON CONFLICT (id) DO UPDATE 
        SET lesson_id = EXCLUDED.lesson_id,
            name = EXCLUDED.name,
            resource_type = EXCLUDED.resource_type,
            url = EXCLUDED.url
        """,
        """
        INSERT INTO enrollments (id, user_id, course_id, status, enrolled_at, completed_at)
        VALUES 
            (1, 2, 1, 'ACTIVE', NOW() - INTERVAL '3 days', NULL),
            (2, 2, 2, 'COMPLETED', NOW() - INTERVAL '10 days', NOW() - INTERVAL '1 day')
        ON CONFLICT (id) DO UPDATE 
        SET user_id = EXCLUDED.user_id,
            course_id = EXCLUDED.course_id,
            status = EXCLUDED.status,
            enrolled_at = EXCLUDED.enrolled_at,
            completed_at = EXCLUDED.completed_at
        """,
        "SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1)) FROM users",
        "SELECT setval(pg_get_serial_sequence('courses', 'id'), COALESCE(MAX(id), 1)) FROM courses",
        "SELECT setval(pg_get_serial_sequence('lessons', 'id'), COALESCE(MAX(id), 1)) FROM lessons",
        "SELECT setval(pg_get_serial_sequence('resources', 'id'), COALESCE(MAX(id), 1)) FROM resources",
        "SELECT setval(pg_get_serial_sequence('enrollments', 'id'), COALESCE(MAX(id), 1)) FROM enrollments",
    ]

    with engine.begin() as conn:
        for stmt in sql_statements:
            conn.execute(text(stmt))

    print("[+] Hoàn tất seed data thành công!")

    # Sinh JWT token cho học viên (user_id = 2)
    student_token = create_access_token(user_id="2", roles=["STUDENT"])
    guest_token = create_access_token(user_id="3", roles=["STUDENT"])

    print("\n" + "=" * 80)
    print("THÔNG TIN DỮ LIỆU ĐÃ SEED VÀ HƯỚNG DẪN TEST VỚI THUNDER CLIENT:")
    print("=" * 80)
    print(f"1. Schema: {schema}")
    print("2. Dữ liệu đã tạo:")
    print("   - Users: id=1 (Mentor), id=2 (Student đã ghi danh), id=3 (Student chưa ghi danh)")
    print("   - Courses: id=1 (PUBLISHED, có tài nguyên), id=2 (PUBLISHED, không tài nguyên), id=3 (DRAFT)")
    print("   - Lessons: id=1 (Bài 1), id=2 (Bài 2) thuộc Course 1")
    print("   - Resources: id=1, 2 (thuộc Bài 1), id=3 (thuộc Bài 2)")
    print("   - Enrollments: id=1 (User 2 ghi danh Course 1, ACTIVE), id=2 (User 2 ghi danh Course 2, COMPLETED)")
    print("-" * 80)
    print("3. TEST API #11: GET /api/v1/courses/{course_id}/resources")
    print("   * Request thành công (200 OK):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/1/resources")
    print("   * Request khóa học chưa publish (404 NOT FOUND):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/3/resources")
    print("   * Request khóa học không có tài nguyên (404 NOT FOUND):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/2/resources")
    print("-" * 80)
    print("4. TEST API #15: GET /api/v1/courses/{course_id}/enrollment-status")
    print("   * Case A - Không truyền token (Guest fallback lấy enrollment bất kỳ của khóa học):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/1/enrollment-status")
    print("   * Case B - Truyền Bearer token của học viên đã ghi danh (User 2):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/1/enrollment-status")
    print("     Header: Authorization: Bearer <TOKEN_USER_2>")
    print(f"     TOKEN_USER_2:\n     {student_token}\n")
    print("   * Case C - Truyền Bearer token của học viên chưa ghi danh (User 3 -> 404):")
    print("     URL:    GET http://localhost:8000/api/v1/courses/1/enrollment-status")
    print("     Header: Authorization: Bearer <TOKEN_USER_3>")
    print(f"     TOKEN_USER_3:\n     {guest_token}")
    print("=" * 80)


if __name__ == "__main__":
    seed_database()
