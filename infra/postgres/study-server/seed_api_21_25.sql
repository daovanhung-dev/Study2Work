-- ==============================================================================
-- Seed data phục vụ kiểm thử thủ công và tự động cho chuỗi API #21 - #25
-- Áp dụng cho schema: hoang_xuan_long (hoặc schema chỉ định qua search_path)
-- ==============================================================================

-- 1. Seed người dùng (users)
INSERT INTO users (id, full_name, email, password_hash, role, avatar_url, phone, status, created_at, updated_at)
VALUES 
    (1, 'Nguyen Van Mentor', 'mentor@study2work.edu.vn', '$2b$12$e8Y5t1examplehashmentor', 'MENTOR', 'https://cdn.example.com/avatars/mentor.png', '0901234567', 'ACTIVE', NOW(), NOW()),
    (2, 'Hoang Xuan Long Student', 'student@study2work.edu.vn', '$2b$12$e8Y5t1examplehashstudent', 'STUDENT', 'https://cdn.example.com/avatars/student.png', '0907654321', 'ACTIVE', NOW(), NOW()),
    (3, 'Le Thi Guest Student', 'guest@study2work.edu.vn', '$2b$12$e8Y5t1examplehashguest', 'STUDENT', 'https://cdn.example.com/avatars/guest.png', '0908889999', 'ACTIVE', NOW(), NOW())
ON CONFLICT (id) DO UPDATE 
SET full_name = EXCLUDED.full_name,
    email = EXCLUDED.email,
    role = EXCLUDED.role,
    avatar_url = EXCLUDED.avatar_url,
    status = EXCLUDED.status,
    updated_at = NOW();

-- 2. Seed khóa học (courses)
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

-- 3. Seed bài học (lessons)
INSERT INTO lessons (id, course_id, name, content, video_url, sort_order, status, created_at, updated_at)
VALUES 
    (1, 1, 'Bài 1: Giới thiệu tổng quan hệ thống Study2Work', 'Nội dung giới thiệu kiến trúc client-server và API contract.', 'https://video.example.com/lessons/lesson_1.mp4', 1, 'PUBLISHED', NOW(), NOW()),
    (2, 1, 'Bài 2: Thiết kế Schema CSDL PostgreSQL', 'Nội dung về thiết kế bảng, khóa chính và foreign key.', 'https://video.example.com/lessons/lesson_2.mp4', 2, 'PUBLISHED', NOW(), NOW()),
    (3, 2, 'Bài 1: Cài đặt môi trường Vue 3', 'Nội dung cài đặt NodeJS, Vite và khởi tạo dự án Vue 3.', 'https://video.example.com/lessons/vue_lesson_1.mp4', 1, 'PUBLISHED', NOW(), NOW()),
    (4, 3, 'Bài 1: Tổng quan về Docker Container', 'Khái niệm container, image và Dockerfile cơ bản.', 'https://video.example.com/lessons/docker_lesson_1.mp4', 1, 'DRAFT', NOW(), NOW())
ON CONFLICT (id) DO UPDATE 
SET course_id = EXCLUDED.course_id,
    name = EXCLUDED.name,
    content = EXCLUDED.content,
    video_url = EXCLUDED.video_url,
    sort_order = EXCLUDED.sort_order,
    status = EXCLUDED.status,
    updated_at = NOW();

-- 4. Seed tài nguyên bài học (resources)
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

-- 5. Seed ghi danh khóa học (enrollments)
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

-- 6. Seed tiến độ học tập (lesson_progress)
INSERT INTO lesson_progress (id, user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at)
VALUES
    (1, 2, 1, 'IN_PROGRESS', 50, NOW(), NULL),
    (2, 2, 3, 'COMPLETED', 100, NOW() - INTERVAL '1 day', NOW() - INTERVAL '1 day')
ON CONFLICT (id) DO UPDATE
SET user_id = EXCLUDED.user_id,
    lesson_id = EXCLUDED.lesson_id,
    status = EXCLUDED.status,
    progress_percent = EXCLUDED.progress_percent,
    last_accessed_at = EXCLUDED.last_accessed_at,
    completed_at = EXCLUDED.completed_at;

-- Đồng bộ sequence cho các bảng
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1)) FROM users;
SELECT setval(pg_get_serial_sequence('courses', 'id'), COALESCE(MAX(id), 1)) FROM courses;
SELECT setval(pg_get_serial_sequence('lessons', 'id'), COALESCE(MAX(id), 1)) FROM lessons;
SELECT setval(pg_get_serial_sequence('resources', 'id'), COALESCE(MAX(id), 1)) FROM resources;
SELECT setval(pg_get_serial_sequence('enrollments', 'id'), COALESCE(MAX(id), 1)) FROM enrollments;
SELECT setval(pg_get_serial_sequence('lesson_progress', 'id'), COALESCE(MAX(id), 1)) FROM lesson_progress;

