-- ============================================================================
-- Fake data: study_dev0.learning_paths
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.learning_paths (
    id,
    slug,
    title,
    summary,
    description,
    level,
    estimated_hours,
    publish_status,
    unlock_mode,
    published_at
) VALUES
    ('20000000-0000-0000-0000-000000000001', 'backend-python-fastapi', 'Backend Python & FastAPI', 'Lộ trình xây dựng API production-ready.', 'Python, FastAPI, PostgreSQL, Docker và quy trình triển khai.', 'INTERMEDIATE', 180, 'PUBLISHED', 'SEQUENTIAL', '2026-06-15 09:00:00+07'),
    ('20000000-0000-0000-0000-000000000002', 'frontend-vue-typescript', 'Frontend Vue 3 & TypeScript', 'Lộ trình phát triển frontend hiện đại.', 'Vue 3, TypeScript, Router, state management và tích hợp REST API.', 'BEGINNER', 150, 'PUBLISHED', 'SEQUENTIAL', '2026-06-16 09:00:00+07'),
    ('20000000-0000-0000-0000-000000000003', 'fullstack-study2work', 'Full-stack Study2Work', 'Lộ trình triển khai sản phẩm web hoàn chỉnh.', 'Kết hợp Backend Python, PostgreSQL, Vue và Docker CI/CD.', 'INTERMEDIATE', 320, 'UPDATED', 'SEQUENTIAL', '2026-06-20 09:00:00+07'),
    ('20000000-0000-0000-0000-000000000004', 'cybersecurity-foundation', 'Nền tảng An ninh mạng', 'Kiến thức nền tảng cho người mới.', 'Mạng máy tính, Linux, OWASP và thực hành bảo mật ứng dụng.', 'BEGINNER', 120, 'DRAFT', 'SEQUENTIAL', NULL)
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS learning_paths_row_count
FROM study_dev0.learning_paths;
