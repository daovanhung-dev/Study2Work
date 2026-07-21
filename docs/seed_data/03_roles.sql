-- ============================================================================
-- Fake data: study_dev0.roles
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.roles (
    id,
    code,
    name,
    scope,
    active
) VALUES
    ('12000000-0000-0000-0000-000000000001', 'LEARNER', 'Học viên', 'STUDY', TRUE),
    ('12000000-0000-0000-0000-000000000002', 'CONTENT_ADMIN', 'Quản trị nội dung', 'CONTENT', TRUE),
    ('12000000-0000-0000-0000-000000000003', 'LEARNER_SUPPORT', 'Hỗ trợ học viên', 'LEARNER_SUPPORT', TRUE),
    ('12000000-0000-0000-0000-000000000004', 'COMMUNITY_MODERATOR', 'Điều phối cộng đồng', 'COMMUNITY', TRUE),
    ('12000000-0000-0000-0000-000000000005', 'REPORT_VIEWER', 'Người xem báo cáo', 'REPORTING', TRUE),
    ('12000000-0000-0000-0000-000000000006', 'SUPER_ADMIN', 'Quản trị hệ thống', 'SYSTEM', TRUE)
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS roles_row_count
FROM study_dev0.roles;
