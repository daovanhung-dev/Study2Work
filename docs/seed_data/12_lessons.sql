-- ============================================================================
-- Fake data: study_dev0.lessons
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.lessons (
    id,
    chapter_id,
    title,
    objective,
    order_index,
    sample_public,
    required,
    completion_condition,
    publish_status
) VALUES
    ('41000000-0000-0000-0000-000000000001', '40000000-0000-0000-0000-000000000001', 'Cài đặt Python và môi trường phát triển', 'Thiết lập Python, venv và IDE.', 1, TRUE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000002', '40000000-0000-0000-0000-000000000001', 'Biến, kiểu dữ liệu và toán tử', 'Thực hành dữ liệu cơ bản trong Python.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000003', '40000000-0000-0000-0000-000000000002', 'Hàm, tham số và phạm vi biến', 'Viết hàm dễ kiểm thử và tái sử dụng.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000004', '40000000-0000-0000-0000-000000000002', 'Class, object và module', 'Tổ chức mã nguồn hướng đối tượng.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000005', '40000000-0000-0000-0000-000000000003', 'Khởi tạo dự án FastAPI', 'Tạo ứng dụng, router và cấu hình dev server.', 1, TRUE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000006', '40000000-0000-0000-0000-000000000003', 'Pydantic model và validation', 'Kiểm tra request/response bằng schema.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000007', '40000000-0000-0000-0000-000000000004', 'Thiết kế CRUD endpoint', 'Xây dựng API CRUD theo REST.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000008', '40000000-0000-0000-0000-000000000004', 'Exception, dependency và middleware', 'Chuẩn hóa lỗi và dependency injection.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000009', '40000000-0000-0000-0000-000000000005', 'SELECT, WHERE và ORDER BY', 'Truy vấn và sắp xếp dữ liệu.', 1, FALSE, TRUE, 'VIEW_CONTENT', 'UPDATED'),
    ('41000000-0000-0000-0000-000000000010', '40000000-0000-0000-0000-000000000005', 'JOIN và GROUP BY', 'Kết hợp bảng và tổng hợp dữ liệu.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'UPDATED'),
    ('41000000-0000-0000-0000-000000000011', '40000000-0000-0000-0000-000000000006', 'Thiết kế schema và constraint', 'Chuẩn hóa bảng, khóa và ràng buộc.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'UPDATED'),
    ('41000000-0000-0000-0000-000000000012', '40000000-0000-0000-0000-000000000006', 'Index, transaction và EXPLAIN', 'Tối ưu truy vấn và xử lý transaction.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'UPDATED'),
    ('41000000-0000-0000-0000-000000000013', '40000000-0000-0000-0000-000000000007', 'Component và template Vue', 'Xây dựng component tái sử dụng.', 1, TRUE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000014', '40000000-0000-0000-0000-000000000007', 'ref, reactive và computed', 'Quản lý reactive state.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000015', '40000000-0000-0000-0000-000000000008', 'Pinia store', 'Tổ chức state dùng chung.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000016', '40000000-0000-0000-0000-000000000008', 'Vue Router và gọi REST API', 'Điều hướng và tích hợp backend.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000017', '40000000-0000-0000-0000-000000000009', 'JSX và functional component', 'Cấu trúc component React.', 1, FALSE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000018', '40000000-0000-0000-0000-000000000009', 'Props, event và form', 'Trao đổi dữ liệu giữa component.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000019', '40000000-0000-0000-0000-000000000010', 'useState và useEffect', 'Quản lý state và side effect.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000020', '40000000-0000-0000-0000-000000000010', 'Context và custom hooks', 'Tái sử dụng logic trong React.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000021', '40000000-0000-0000-0000-000000000011', 'Docker image và container', 'Đóng gói ứng dụng thành container.', 1, FALSE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000022', '40000000-0000-0000-0000-000000000011', 'Volume, network và compose', 'Kết nối dịch vụ bằng Docker Compose.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000023', '40000000-0000-0000-0000-000000000012', 'Thiết kế pipeline CI', 'Chạy lint, test và build tự động.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000024', '40000000-0000-0000-0000-000000000012', 'Triển khai CD', 'Tự động phát hành qua môi trường.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000025', '40000000-0000-0000-0000-000000000013', 'CIA triad và threat model', 'Nhận diện tài sản, mối đe dọa và rủi ro.', 1, FALSE, TRUE, 'VIEW_CONTENT', 'DRAFT'),
    ('41000000-0000-0000-0000-000000000026', '40000000-0000-0000-0000-000000000013', 'Linux và network căn bản', 'Quyền file, process và giao thức mạng.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'DRAFT'),
    ('41000000-0000-0000-0000-000000000027', '40000000-0000-0000-0000-000000000014', 'OWASP Top 10', 'Các nhóm lỗ hổng web phổ biến.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'DRAFT'),
    ('41000000-0000-0000-0000-000000000028', '40000000-0000-0000-0000-000000000014', 'Secure coding', 'Validation, authentication và secret management.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'DRAFT'),
    ('41000000-0000-0000-0000-000000000029', '40000000-0000-0000-0000-000000000015', 'Commit, branch và merge', 'Thao tác Git trong dự án thực tế.', 1, TRUE, TRUE, 'VIEW_CONTENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000030', '40000000-0000-0000-0000-000000000015', 'Resolve conflict', 'Phân tích và xử lý xung đột.', 2, FALSE, TRUE, 'VIDEO_PERCENT', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000031', '40000000-0000-0000-0000-000000000016', 'Pull request và code review', 'Quy trình hợp nhất mã nguồn.', 1, FALSE, TRUE, 'SELF_MARKED_DONE', 'PUBLISHED'),
    ('41000000-0000-0000-0000-000000000032', '40000000-0000-0000-0000-000000000016', 'Tag, release và GitHub Actions', 'Quản lý phiên bản và tự động hóa.', 2, FALSE, TRUE, 'REQUIRED_EXERCISE_PASSED', 'PUBLISHED')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS lessons_row_count
FROM study_dev0.lessons;
