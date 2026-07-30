-- ============================================================================
-- Fake data: study_dev0.onboarding_records
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.onboarding_records (
    id,
    user_id,
    programming_level,
    known_technologies,
    main_goal,
    sub_goals,
    weekly_study_hours,
    selected_learning_path_id,
    status,
    current_step,
    confirmed_at
) VALUES
    ('21000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'INTERMEDIATE', ARRAY['Python', 'FastAPI', 'Vue.js']::TEXT[], 'Full-stack Developer', ARRAY['Hoàn thành dự án S2W', 'Nắm vững PostgreSQL']::TEXT[], 20, '20000000-0000-0000-0000-000000000003', 'COMPLETED', 5, '2026-06-10 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 'BASIC', ARRAY['Python', 'Git']::TEXT[], 'Backend Developer', ARRAY['Viết REST API', 'Học Docker']::TEXT[], 14, '20000000-0000-0000-0000-000000000001', 'COMPLETED', 5, '2026-06-11 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000003', 'BASIC', ARRAY['JavaScript', 'HTML', 'CSS']::TEXT[], 'Frontend Developer', ARRAY['Vue 3', 'TypeScript']::TEXT[], 12, '20000000-0000-0000-0000-000000000002', 'COMPLETED', 5, '2026-06-12 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000004', 'BEGINNER', ARRAY['HTML', 'CSS']::TEXT[], 'Web Developer', ARRAY['JavaScript cơ bản', 'Vue cơ bản']::TEXT[], 10, '20000000-0000-0000-0000-000000000002', 'IN_PROGRESS', 3, NULL),
    ('21000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000005', 'BEGINNER', ARRAY['Python']::TEXT[], 'Backend Developer', ARRAY['FastAPI']::TEXT[], 8, NULL, 'NOT_STARTED', 0, NULL),
    ('21000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000006', 'INTERMEDIATE', ARRAY['Node.js', 'SQL']::TEXT[], 'Database Developer', ARRAY['PostgreSQL', 'Tối ưu truy vấn']::TEXT[], 6, '20000000-0000-0000-0000-000000000001', 'COMPLETED', 5, '2026-06-15 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000007', 'INTERMEDIATE', ARRAY['Python', 'SQL', 'Docker']::TEXT[], 'Backend Developer', ARRAY['Hoàn thành lộ trình Backend']::TEXT[], 18, '20000000-0000-0000-0000-000000000001', 'COMPLETED', 5, '2026-06-16 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000008', 'BASIC', ARRAY['JavaScript', 'React']::TEXT[], 'Full-stack Developer', ARRAY['FastAPI', 'PostgreSQL']::TEXT[], 15, '20000000-0000-0000-0000-000000000003', 'COMPLETED', 5, '2026-06-17 20:00:00+07'),
    ('21000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000009', 'BEGINNER', ARRAY[]::TEXT[], 'Khám phá lập trình', ARRAY['Python cơ bản']::TEXT[], 5, NULL, 'NOT_STARTED', 0, NULL),
    ('21000000-0000-0000-0000-000000000010', '10000000-0000-0000-0000-000000000010', 'INTERMEDIATE', ARRAY['Python', 'Vue.js', 'PostgreSQL']::TEXT[], 'Full-stack Developer', ARRAY['Hoàn thành capstone']::TEXT[], 16, '20000000-0000-0000-0000-000000000003', 'COMPLETED', 5, '2026-06-18 20:00:00+07')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS onboarding_records_row_count
FROM study_dev0.onboarding_records;
