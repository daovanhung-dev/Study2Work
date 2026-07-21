-- ============================================================================
-- Fake data: study_dev0.community_groups
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.community_groups (
    id,
    name,
    scope_type,
    scope_id,
    join_link,
    status,
    rules,
    moderator_id
) VALUES
    ('60000000-0000-0000-0000-000000000001', 'Cộng đồng Study2Work', 'GLOBAL', NULL, 'https://zalo.me/g/s2w-global-demo', 'ACTIVE', 'Tôn trọng thành viên; không spam; không chia sẻ nội dung vi phạm.', '10000000-0000-0000-0000-000000000012'),
    ('60000000-0000-0000-0000-000000000002', 'Backend Python & FastAPI', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000001', 'https://zalo.me/g/s2w-backend-demo', 'ACTIVE', 'Trao đổi đúng chủ đề Backend; che thông tin nhạy cảm khi đăng lỗi.', '10000000-0000-0000-0000-000000000012'),
    ('60000000-0000-0000-0000-000000000003', 'Frontend Vue & TypeScript', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000002', 'https://zalo.me/g/s2w-frontend-demo', 'ACTIVE', 'Trao đổi Vue, React và frontend engineering.', '10000000-0000-0000-0000-000000000012'),
    ('60000000-0000-0000-0000-000000000004', 'Full-stack Study2Work', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000003', 'https://zalo.me/g/s2w-fullstack-demo', 'ACTIVE', 'Thảo luận tích hợp Backend, Frontend và DevOps.', '10000000-0000-0000-0000-000000000011'),
    ('60000000-0000-0000-0000-000000000005', 'FastAPI REST API Support', 'COURSE', '30000000-0000-0000-0000-000000000002', 'https://zalo.me/g/s2w-fastapi-demo', 'PAUSED', 'Nhóm hỗ trợ riêng cho khóa FastAPI.', '10000000-0000-0000-0000-000000000012'),
    ('60000000-0000-0000-0000-000000000006', 'Chủ đề Git và DevOps', 'TOPIC', '60000000-0000-0000-0000-000000001001', 'https://zalo.me/g/s2w-devops-demo', 'ACTIVE', 'Trao đổi Git, Docker, CI/CD và release.', '10000000-0000-0000-0000-000000000011')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS community_groups_row_count
FROM study_dev0.community_groups;
