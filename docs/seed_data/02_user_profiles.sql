-- ============================================================================
-- Fake data: study_dev0.user_profiles
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.user_profiles (
    id,
    user_id,
    avatar_url,
    city,
    school_or_company,
    current_major_or_job,
    learning_goal,
    known_technologies,
    weekly_study_hours,
    updated_at
) VALUES
    ('11000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'https://cdn.s2w.dev/avatars/u01.png', 'Hà Nội', 'VNUA', 'Sinh viên CNTT', 'Trở thành Full-stack Developer', ARRAY['Python', 'FastAPI', 'Vue.js', 'PostgreSQL']::TEXT[], 20, '2026-07-20 09:00:00+07'),
    ('11000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 'https://cdn.s2w.dev/avatars/u02.png', 'Hà Nội', 'Đại học Công nghiệp Hà Nội', 'Sinh viên năm 3', 'Backend Python', ARRAY['Python', 'Git']::TEXT[], 14, '2026-07-20 09:10:00+07'),
    ('11000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000003', 'https://cdn.s2w.dev/avatars/u03.png', 'Hải Phòng', 'Đại học Hàng Hải', 'Frontend Intern', 'Frontend Vue/React', ARRAY['JavaScript', 'HTML', 'CSS']::TEXT[], 12, '2026-07-19 18:30:00+07'),
    ('11000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000004', NULL, 'Đà Nẵng', 'Đại học Bách khoa Đà Nẵng', 'Sinh viên năm 2', 'Học lập trình web từ cơ bản', ARRAY['HTML', 'CSS']::TEXT[], 10, '2026-07-18 11:00:00+07'),
    ('11000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000005', NULL, 'Hồ Chí Minh', 'Cao đẳng FPT Polytechnic', 'Sinh viên', 'Xây dựng REST API', ARRAY['Python']::TEXT[], 8, '2026-07-17 13:20:00+07'),
    ('11000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000006', NULL, 'Bắc Ninh', 'Công ty DemoTech', 'Junior Developer', 'Củng cố PostgreSQL', ARRAY['Node.js', 'SQL']::TEXT[], 6, '2026-07-16 15:00:00+07'),
    ('11000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000007', 'https://cdn.s2w.dev/avatars/u07.png', 'Hà Nội', 'Đại học Thủy Lợi', 'Sinh viên năm 4', 'Hoàn thành lộ trình Backend', ARRAY['Python', 'SQL', 'Docker']::TEXT[], 18, '2026-07-20 19:00:00+07'),
    ('11000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000008', NULL, 'Thái Nguyên', 'Đại học CNTT&TT', 'Sinh viên', 'Full-stack Developer', ARRAY['JavaScript', 'React']::TEXT[], 15, '2026-07-18 08:00:00+07'),
    ('11000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000009', NULL, 'Nghệ An', 'THPT Demo', 'Học sinh', 'Tìm hiểu lập trình', ARRAY[]::TEXT[], 5, '2026-07-10 08:30:00+07'),
    ('11000000-0000-0000-0000-000000000010', '10000000-0000-0000-0000-000000000010', 'https://cdn.s2w.dev/avatars/u10.png', 'Hà Nội', 'VNUA', 'Sinh viên CNTT', 'Hoàn thành dự án Full-stack', ARRAY['Python', 'Vue.js', 'PostgreSQL']::TEXT[], 16, '2026-07-21 07:45:00+07'),
    ('11000000-0000-0000-0000-000000000011', '10000000-0000-0000-0000-000000000011', NULL, 'Hà Nội', 'Study2Work', 'System Administrator', 'Quản trị nền tảng', ARRAY['PostgreSQL', 'Docker', 'Python']::TEXT[], 10, '2026-07-21 08:00:00+07'),
    ('11000000-0000-0000-0000-000000000012', '10000000-0000-0000-0000-000000000012', NULL, 'Hà Nội', 'Study2Work', 'Learning Mentor', 'Hỗ trợ học viên', ARRAY['Python', 'FastAPI', 'Git']::TEXT[], 12, '2026-07-21 08:10:00+07')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS user_profiles_row_count
FROM study_dev0.user_profiles;
