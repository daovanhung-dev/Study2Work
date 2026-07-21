-- ============================================================================
-- Fake data: study_dev0.notifications
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.notifications (
    id,
    user_id,
    type,
    title,
    body,
    priority,
    read_status,
    action_url,
    created_at,
    read_at
) VALUES
    ('51000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000001', 'SYSTEM', 'Chào mừng đến Study2Work', 'Hồ sơ của bạn đã sẵn sàng để bắt đầu học.', 'NORMAL', 'READ', '/dashboard', '2026-07-01 08:00:00+07', '2026-07-01 08:05:00+07'),
    ('51000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000002', 'LEARNING_REMINDER', 'Tiếp tục khóa FastAPI', 'Bạn đang hoàn thành 45% khóa FastAPI REST API.', 'NORMAL', 'UNREAD', '/courses/fastapi-rest-api', '2026-07-21 07:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000002', 'REVIEW_RESULT', 'Bài Python đã được chấm', 'Bài tập biến và kiểu dữ liệu đạt 85 điểm.', 'HIGH', 'READ', '/submissions/44000000-0000-0000-0000-000000000002', '2026-06-17 09:05:00+07', '2026-06-17 09:10:00+07'),
    ('51000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000002', 'ASSIGNMENT', 'Bài nộp đang được đánh giá', 'Thư viện hàm tiện ích đang chờ mentor phản hồi.', 'NORMAL', 'UNREAD', '/submissions/44000000-0000-0000-0000-000000000003', '2026-07-20 21:05:00+07', NULL),
    ('51000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000003', 'LEARNING_REMINDER', 'Hoàn thành Vue Router', 'Bạn còn một bài tập để hoàn thành chương State và Router.', 'NORMAL', 'UNREAD', '/exercises/43000000-0000-0000-0000-000000000009', '2026-07-21 07:10:00+07', NULL),
    ('51000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000004', 'SYSTEM', 'Tiếp tục onboarding', 'Bạn đang ở bước 3 trong quy trình onboarding.', 'NORMAL', 'UNREAD', '/onboarding', '2026-07-20 08:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000007', '10000000-0000-0000-0000-000000000005', 'SYSTEM', 'Hãy hoàn tất onboarding', 'Chọn mục tiêu và lộ trình phù hợp để bắt đầu học.', 'NORMAL', 'UNREAD', '/onboarding', '2026-07-19 08:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000008', '10000000-0000-0000-0000-000000000006', 'SECURITY', 'Tài khoản đang tạm ngừng', 'Liên hệ bộ phận hỗ trợ để xác minh tài khoản.', 'URGENT', 'READ', '/support', '2026-07-16 15:00:00+07', '2026-07-16 15:10:00+07'),
    ('51000000-0000-0000-0000-000000000009', '10000000-0000-0000-0000-000000000007', 'CONTENT_UPDATE', 'Khóa PostgreSQL có nội dung mới', 'Bài Index, transaction và EXPLAIN đã được cập nhật.', 'HIGH', 'READ', '/lessons/41000000-0000-0000-0000-000000000012', '2026-07-12 10:00:00+07', '2026-07-12 10:15:00+07'),
    ('51000000-0000-0000-0000-000000000010', '10000000-0000-0000-0000-000000000007', 'SYSTEM', 'Hoàn thành lộ trình Backend', 'Chúc mừng bạn đã hoàn thành lộ trình Backend Python & FastAPI.', 'HIGH', 'READ', '/learning-paths/20000000-0000-0000-0000-000000000001', '2026-07-10 17:05:00+07', '2026-07-10 17:10:00+07'),
    ('51000000-0000-0000-0000-000000000011', '10000000-0000-0000-0000-000000000008', 'LEARNING_REMINDER', 'Lộ trình Full-stack đã sẵn sàng', 'Bạn có thể kích hoạt lộ trình và bắt đầu khóa Python.', 'NORMAL', 'UNREAD', '/learning-paths/20000000-0000-0000-0000-000000000003', '2026-07-20 09:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000012', '10000000-0000-0000-0000-000000000009', 'SECURITY', 'Xác thực tài khoản', 'Vui lòng xác thực email hoặc số điện thoại để tiếp tục.', 'HIGH', 'UNREAD', '/verify-contact', '2026-07-10 08:31:00+07', NULL),
    ('51000000-0000-0000-0000-000000000013', '10000000-0000-0000-0000-000000000010', 'REVIEW_RESULT', 'Bài FastAPI cần chỉnh sửa', 'Bạn cần ôn lại dependency injection và middleware.', 'HIGH', 'UNREAD', '/submissions/44000000-0000-0000-0000-000000000013', '2026-07-10 20:02:00+07', NULL),
    ('51000000-0000-0000-0000-000000000014', '10000000-0000-0000-0000-000000000010', 'LEARNING_REMINDER', 'Tiếp tục FastAPI', 'Hoàn thành bài Pydantic model và validation.', 'NORMAL', 'UNREAD', '/lessons/41000000-0000-0000-0000-000000000006', '2026-07-21 07:35:00+07', NULL),
    ('51000000-0000-0000-0000-000000000015', '10000000-0000-0000-0000-000000000011', 'ADMIN_MANUAL', 'Báo cáo vận hành tháng 7', 'Dashboard báo cáo đã được cập nhật dữ liệu mới.', 'NORMAL', 'READ', '/admin/reports', '2026-07-21 08:00:00+07', '2026-07-21 08:02:00+07'),
    ('51000000-0000-0000-0000-000000000016', '10000000-0000-0000-0000-000000000012', 'ASSIGNMENT', 'Có bài nộp mới cần kiểm tra', 'Học viên Nguyễn Minh Anh vừa nộp bài thư viện hàm.', 'HIGH', 'UNREAD', '/admin/submissions/44000000-0000-0000-0000-000000000003', '2026-07-20 21:01:00+07', NULL),
    ('51000000-0000-0000-0000-000000000017', '10000000-0000-0000-0000-000000000012', 'COMMUNITY', 'Nhóm Backend có thành viên mới', 'Lượt mở liên kết nhóm Backend tăng trong tuần này.', 'LOW', 'UNREAD', '/admin/community/60000000-0000-0000-0000-000000000002', '2026-07-21 08:10:00+07', NULL),
    ('51000000-0000-0000-0000-000000000018', '10000000-0000-0000-0000-000000000001', 'MANDATORY_NOTICE', 'Bảo trì hệ thống', 'Hệ thống bảo trì từ 23:00 đến 23:30 ngày 25/07/2026.', 'URGENT', 'UNREAD', '/announcements/maintenance', '2026-07-21 09:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000019', '10000000-0000-0000-0000-000000000002', 'COMMUNITY', 'Tham gia cộng đồng Backend', 'Nhóm Zalo Backend Python đang hoạt động.', 'NORMAL', 'UNREAD', '/community/60000000-0000-0000-0000-000000000002', '2026-07-20 12:00:00+07', NULL),
    ('51000000-0000-0000-0000-000000000020', '10000000-0000-0000-0000-000000000003', 'CONTENT_UPDATE', 'Cập nhật khóa Vue 3', 'Bài Pinia store đã bổ sung ví dụ mới.', 'NORMAL', 'HIDDEN', '/lessons/41000000-0000-0000-0000-000000000015', '2026-07-18 10:00:00+07', NULL)
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS notifications_row_count
FROM study_dev0.notifications;
