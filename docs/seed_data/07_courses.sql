-- ============================================================================
-- Fake data: study_dev0.courses
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.courses (
    id,
    slug,
    title,
    summary,
    level,
    estimated_minutes,
    publish_status,
    published_at
) VALUES
    ('30000000-0000-0000-0000-000000000001', 'python-fundamentals', 'Python Fundamentals', 'Nền tảng Python cho lập trình backend.', 'BEGINNER', 1200, 'PUBLISHED', '2026-06-01 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000002', 'fastapi-rest-api', 'FastAPI REST API', 'Thiết kế và xây dựng REST API với FastAPI.', 'INTERMEDIATE', 1500, 'PUBLISHED', '2026-06-02 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000003', 'postgresql-for-developers', 'PostgreSQL for Developers', 'SQL, thiết kế schema, index và transaction.', 'INTERMEDIATE', 1200, 'UPDATED', '2026-06-03 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000004', 'vue3-typescript', 'Vue 3 & TypeScript', 'Xây dựng frontend với Vue Composition API.', 'BEGINNER', 1400, 'PUBLISHED', '2026-06-04 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000005', 'react-typescript', 'React & TypeScript', 'React Hooks, state và kiến trúc component.', 'INTERMEDIATE', 1300, 'PUBLISHED', '2026-06-05 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000006', 'docker-cicd', 'Docker & CI/CD', 'Container hóa và tự động hóa triển khai.', 'INTERMEDIATE', 900, 'PUBLISHED', '2026-06-06 09:00:00+07'),
    ('30000000-0000-0000-0000-000000000007', 'cybersecurity-fundamentals', 'Cybersecurity Fundamentals', 'Mạng, Linux, OWASP và bảo mật ứng dụng.', 'BEGINNER', 1100, 'DRAFT', NULL),
    ('30000000-0000-0000-0000-000000000008', 'git-github-workflow', 'Git & GitHub Workflow', 'Quản lý mã nguồn và quy trình cộng tác.', 'BEGINNER', 600, 'PUBLISHED', '2026-06-08 09:00:00+07')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS courses_row_count
FROM study_dev0.courses;
