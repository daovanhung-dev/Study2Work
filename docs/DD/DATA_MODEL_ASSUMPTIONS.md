# Data Model Assumptions

BD mô tả mô hình nghiệp vụ nhưng không kèm ERD hoặc schema database đã chốt. Các ánh xạ trong bộ DD dùng tên bảng/aggregate đề xuất để backend có thể triển khai nhất quán:

- Identity: `users`, `user_profiles`, `contact_verifications`, `auth_sessions`, `refresh_tokens`.
- Learning: `learning_paths`, `learner_learning_paths`, `courses`, `course_modules`, `lessons`, `lesson_resources`.
- Assessment: `exercises`, `exercise_questions`, `exercise_attempts`, `exercise_submissions`, `submission_reviews`.
- Progress: `learner_path_progress`, `course_progress`, `lesson_progress`, `learning_events`.
- Community: `community_groups`, `community_group_scopes`, `community_link_open_logs`, `community_reports`.
- Operations: `notifications`, `notification_deliveries`, `support_requests`, `learner_path_exceptions`, `audit_logs`, `report_snapshots`.

Tên bảng có thể đổi ở implementation, nhưng contract API, trạng thái và rule nghiệp vụ không được đổi ngầm.
