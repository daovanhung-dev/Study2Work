-- ============================================================================
-- Fake data: study_dev0.support_requests
-- Có thể chạy lại nhiều lần nhờ ON CONFLICT DO NOTHING.
-- ============================================================================

SET search_path TO study_dev0, public;

INSERT INTO study_dev0.support_requests (
    id,
    user_id,
    type,
    reason,
    current_learning_path_id,
    target_learning_path_id,
    current_learning_path_enrollment_id,
    status,
    admin_decision,
    resolved_at
) VALUES
    ('70000000-0000-0000-0000-000000000001', '10000000-0000-0000-0000-000000000002', 'CHANGE_PATH', 'Muốn chuyển sang lộ trình Full-stack sau khi hoàn thành FastAPI.', '20000000-0000-0000-0000-000000000001', '20000000-0000-0000-0000-000000000003', '32000000-0000-0000-0000-000000000002', 'OPEN', NULL, NULL),
    ('70000000-0000-0000-0000-000000000002', '10000000-0000-0000-0000-000000000004', 'RESET_PATH', 'Muốn làm lại onboarding và chọn lại mục tiêu.', '20000000-0000-0000-0000-000000000002', NULL, '32000000-0000-0000-0000-000000000004', 'IN_REVIEW', NULL, NULL),
    ('70000000-0000-0000-0000-000000000003', '10000000-0000-0000-0000-000000000006', 'CANCEL_PATH', 'Tạm dừng học trong thời gian xác minh tài khoản.', '20000000-0000-0000-0000-000000000001', NULL, '32000000-0000-0000-0000-000000000005', 'RESOLVED', 'Đã hủy lộ trình theo yêu cầu và bảo toàn lịch sử.', '2026-07-16 15:00:00+07'),
    ('70000000-0000-0000-0000-000000000004', '10000000-0000-0000-0000-000000000007', 'PROGRESS_RESET', 'Yêu cầu mở lại bài SQL để luyện tập.', '20000000-0000-0000-0000-000000000001', NULL, '32000000-0000-0000-0000-000000000006', 'APPROVED', 'Đã mở lại quyền luyện tập, không thay đổi trạng thái hoàn thành.', '2026-07-15 10:00:00+07'),
    ('70000000-0000-0000-0000-000000000005', '10000000-0000-0000-0000-000000000008', 'OTHER', 'Cần tư vấn thứ tự học phù hợp với React hiện có.', '20000000-0000-0000-0000-000000000003', NULL, '32000000-0000-0000-0000-000000000007', 'OPEN', NULL, NULL),
    ('70000000-0000-0000-0000-000000000006', '10000000-0000-0000-0000-000000000010', 'CHANGE_PATH', 'Muốn chuyển từ Full-stack sang Backend.', '20000000-0000-0000-0000-000000000003', '20000000-0000-0000-0000-000000000001', '32000000-0000-0000-0000-000000000008', 'REJECTED', 'Từ chối tạm thời vì đang có bài FastAPI cần hoàn thiện.', '2026-07-20 10:00:00+07')
ON CONFLICT DO NOTHING;

SELECT COUNT(*) AS support_requests_row_count
FROM study_dev0.support_requests;
