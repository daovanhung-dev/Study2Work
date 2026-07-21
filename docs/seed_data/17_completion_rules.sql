-- ============================================================================
-- Fake data: study_dev0.completion_rules
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.completion_rules (
    id,
    target_type,
    target_id,
    required_items_only,
    minimum_score,
    minimum_video_percent,
    description
) VALUES
    ('46000000-0000-0000-0000-000000000001', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000001', TRUE, 70, 80, 'Hoàn thành các khóa bắt buộc và đạt tối thiểu 70 điểm.'),
    ('46000000-0000-0000-0000-000000000002', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000002', TRUE, 70, 80, 'Hoàn thành khóa Vue, React và Git.'),
    ('46000000-0000-0000-0000-000000000003', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000003', TRUE, 75, 80, 'Hoàn thành toàn bộ nội dung bắt buộc của lộ trình Full-stack.'),
    ('46000000-0000-0000-0000-000000000004', 'LEARNING_PATH', '20000000-0000-0000-0000-000000000004', TRUE, 70, 80, 'Hoàn thành các nội dung bảo mật bắt buộc.'),
    ('46000000-0000-0000-0000-000000000005', 'COURSE', '30000000-0000-0000-0000-000000000001', TRUE, 70, 80, 'Hoàn thành bài học và bài tập Python.'),
    ('46000000-0000-0000-0000-000000000006', 'COURSE', '30000000-0000-0000-0000-000000000002', TRUE, 70, 80, 'Hoàn thành dự án API CRUD.'),
    ('46000000-0000-0000-0000-000000000007', 'COURSE', '30000000-0000-0000-0000-000000000003', TRUE, 70, 80, 'Hoàn thành bài tập SQL và thiết kế database.'),
    ('46000000-0000-0000-0000-000000000008', 'COURSE', '30000000-0000-0000-0000-000000000004', TRUE, 70, 80, 'Hoàn thành Vue component và ứng dụng Router.'),
    ('46000000-0000-0000-0000-000000000009', 'COURSE', '30000000-0000-0000-0000-000000000005', TRUE, 70, 80, 'Hoàn thành dự án React Hooks.'),
    ('46000000-0000-0000-0000-000000000010', 'COURSE', '30000000-0000-0000-0000-000000000006', TRUE, 70, 80, 'Hoàn thành Dockerfile và pipeline CI/CD.'),
    ('46000000-0000-0000-0000-000000000011', 'COURSE', '30000000-0000-0000-0000-000000000007', TRUE, 70, 80, 'Hoàn thành quiz và bài thực hành bảo mật.'),
    ('46000000-0000-0000-0000-000000000012', 'COURSE', '30000000-0000-0000-0000-000000000008', TRUE, 70, 80, 'Hoàn thành quiz Git và quy trình GitHub.')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS completion_rules_row_count
FROM study_dev0.completion_rules;
