-- ============================================================================
-- Fake data: study_dev0.chapters
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.chapters (
    id,
    course_id,
    title,
    objective,
    order_index,
    required,
    unlock_condition
) VALUES
    ('40000000-0000-0000-0000-000000000001', '30000000-0000-0000-0000-000000000001', 'Cú pháp và kiểu dữ liệu', 'Nắm cú pháp Python, biến và kiểu dữ liệu.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000002', '30000000-0000-0000-0000-000000000001', 'Hàm và lập trình hướng đối tượng', 'Xây dựng hàm, class và module.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000003', '30000000-0000-0000-0000-000000000002', 'FastAPI cơ bản', 'Khởi tạo ứng dụng và định nghĩa endpoint.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000004', '30000000-0000-0000-0000-000000000002', 'Xây dựng REST API', 'CRUD, validation và xử lý lỗi.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000005', '30000000-0000-0000-0000-000000000003', 'SQL nền tảng', 'SELECT, JOIN, GROUP BY và transaction.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000006', '30000000-0000-0000-0000-000000000003', 'Thiết kế và tối ưu PostgreSQL', 'Schema, index và execution plan.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000007', '30000000-0000-0000-0000-000000000004', 'Vue Composition API', 'Component và reactive state.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000008', '30000000-0000-0000-0000-000000000004', 'State và Router', 'Pinia, Vue Router và gọi API.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000009', '30000000-0000-0000-0000-000000000005', 'React Fundamentals', 'JSX, component và props.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000010', '30000000-0000-0000-0000-000000000005', 'Hooks và State Management', 'Hooks và quản lý state.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000011', '30000000-0000-0000-0000-000000000006', 'Docker cơ bản', 'Image, container và volume.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000012', '30000000-0000-0000-0000-000000000006', 'CI/CD', 'Pipeline kiểm thử và triển khai.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000013', '30000000-0000-0000-0000-000000000007', 'Nền tảng an ninh mạng', 'CIA triad, network và Linux.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000014', '30000000-0000-0000-0000-000000000007', 'Web Security', 'OWASP Top 10 và secure coding.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED'),
    ('40000000-0000-0000-0000-000000000015', '30000000-0000-0000-0000-000000000008', 'Git cơ bản', 'Commit, branch và merge.', 1, TRUE, 'ALWAYS'),
    ('40000000-0000-0000-0000-000000000016', '30000000-0000-0000-0000-000000000008', 'Quy trình GitHub', 'Pull request, review và release.', 2, TRUE, 'PREVIOUS_CHAPTER_COMPLETED')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS chapters_row_count
FROM study_dev0.chapters;
