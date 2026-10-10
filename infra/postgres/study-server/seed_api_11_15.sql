-- ==============================================================================
-- Seed Data for API #11 (/courses/{course_id}/resources) 
-- and API #15 (/courses/{course_id}/enrollment-status)
-- Schema: hoang_xuan_long (hoặc schema tùy cấu hình)
-- ==============================================================================

-- Thiết lập search_path tới schema của bạn:
SET search_path TO hoang_xuan_long, public;

-- 1. Seed Users (Mentor và Học viên)
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
    updated_at = NOW();

-- 2. Seed Courses
-- Course 1: PUBLISHED (Dùng cho API 11 & API 15 - có bài học, tài nguyên và ghi danh)
-- Course 2: PUBLISHED (Không có tài nguyên - dùng test trường hợp API 11 trả 404, có enrollment COMPLETED)
-- Course 3: DRAFT (Chưa publish - dùng test trường hợp API 11 kiểm tra status != PUBLISHED trả 404)
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
    updated_at = NOW();

-- 3. Seed Lessons (Thuộc Course 1)
INSERT INTO lessons (id, course_id, name, content, video_url, sort_order, status, created_at, updated_at)
VALUES 
    (1, 1, 'Bài 1: Giới thiệu tổng quan hệ thống Study2Work', 'Nội dung giới thiệu kiến trúc client-server và API contract.', 'https://video.example.com/lessons/lesson_1.mp4', 1, 'PUBLISHED', NOW(), NOW()),
    (2, 1, 'Bài 2: Thiết kế Schema CSDL PostgreSQL', 'Nội dung về thiết kế bảng, khóa chính và foreign key.', 'https://video.example.com/lessons/lesson_2.mp4', 2, 'PUBLISHED', NOW(), NOW())
ON CONFLICT (id) DO UPDATE 
SET course_id = EXCLUDED.course_id,
    name = EXCLUDED.name,
    status = EXCLUDED.status,
    updated_at = NOW();

-- 4. Seed Resources (Tài nguyên cho Bài 1 và Bài 2 - phục vụ API #11)
INSERT INTO resources (id, lesson_id, name, resource_type, url, created_at)
VALUES 
    (1, 1, 'Tai_lieu_kien_truc_study2work.pdf', 'DOCUMENT', 'https://cdn.example.com/resources/Tai_lieu_kien_truc_study2work.pdf', NOW()),
    (2, 1, 'Source_code_mau_bai_1.zip', 'ARCHIVE', 'https://cdn.example.com/resources/Source_code_mau_bai_1.zip', NOW()),
    (3, 2, 'Slide_thiet_ke_database.pdf', 'DOCUMENT', 'https://cdn.example.com/resources/Slide_thiet_ke_database.pdf', NOW())
ON CONFLICT (id) DO UPDATE 
SET lesson_id = EXCLUDED.lesson_id,
    name = EXCLUDED.name,
    resource_type = EXCLUDED.resource_type,
    url = EXCLUDED.url;

-- 5. Seed Enrollments (Trạng thái ghi danh - phục vụ API #15)
-- User 2 ghi danh Course 1: status ACTIVE
-- User 2 ghi danh Course 2: status COMPLETED
INSERT INTO enrollments (id, user_id, course_id, status, enrolled_at, completed_at)
VALUES 
    (1, 2, 1, 'ACTIVE', NOW() - INTERVAL '3 days', NULL),
    (2, 2, 2, 'COMPLETED', NOW() - INTERVAL '10 days', NOW() - INTERVAL '1 day')
ON CONFLICT (id) DO UPDATE 
SET user_id = EXCLUDED.user_id,
    course_id = EXCLUDED.course_id,
    status = EXCLUDED.status,
    enrolled_at = EXCLUDED.enrolled_at,
    completed_at = EXCLUDED.completed_at;

-- 6. Đồng bộ hóa Primary Key sequence sau khi chèn dữ liệu tường minh
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1)) FROM users;
SELECT setval(pg_get_serial_sequence('courses', 'id'), COALESCE(MAX(id), 1)) FROM courses;
SELECT setval(pg_get_serial_sequence('lessons', 'id'), COALESCE(MAX(id), 1)) FROM lessons;
SELECT setval(pg_get_serial_sequence('resources', 'id'), COALESCE(MAX(id), 1)) FROM resources;
SELECT setval(pg_get_serial_sequence('enrollments', 'id'), COALESCE(MAX(id), 1)) FROM enrollments;

