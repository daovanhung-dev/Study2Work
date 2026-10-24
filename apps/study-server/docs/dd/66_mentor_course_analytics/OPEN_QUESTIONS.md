# Open Questions — Study API #66

Status: Draft — Needs Confirmation. Các câu hỏi sau cần được giải quyết trước khi endpoint có thể implementation-ready.

1. **Response conflict:** Catalog trả Page<Course>, còn AC-26 yêu cầu aggregate learning events. Có sửa contract thành CourseLearningAnalytics không?
2. **Metric set:** Có chấp nhận ba metric candidate total_learning_events, students_with_learning_events và last_activity_at không? Có cần breakdown theo event type, learner, ngày hoặc tỷ lệ không?
3. **Event source:** Learning event được tạo/lưu ở đâu? Legacy DDL không có event history; V1-PILOT progress facts và audit/outbox chưa phải nguồn được xác nhận.
4. **Event taxonomy:** Hành vi nào được tính là learning event? Có loại view/start/progress/completion khỏi event count không?
5. **Dedup/retries:** Event có immutable ID nào để chống đếm trùng? Quy tắc xử lý retry và event đến trễ là gì?
6. **Time window:** Request không có from/to; dùng all-time-to-date hay cần bổ sung bộ lọc thời gian?
7. **Student identity:** Event actor được liên kết với Student và course enrollment bằng khóa nào? Có loại tài khoản/record đã xóa hoặc withdrawn không?
8. **Freshness:** Aggregate tính trực tiếp, dùng snapshot hay cache? Freshness/SLA nào được yêu cầu?
9. **Mentor authorization:** JWT principal map đến Mentor ID nào? Mentor được assign course có được xem không? 403/404 privacy order là gì?
10. **Pagination:** Contract Page<Course> có PageMeta nhưng không có page/size request. Nếu giữ response này, semantics và giới hạn ra sao?
11. **Empty course:** Candidate đề xuất count=0 và last_activity_at=null khi không có event; cần xác nhận cùng null serialization.
12. **Group AC-26:** Macro-review #65–#67 đã hoàn tất ở mức tài liệu; xem [VERIFICATION_REPORT](./VERIFICATION_REPORT.md). Còn mở: contract Page<Course>, pagination, event source/metric definitions, shared Mentor authorization/schema/error policy và reconciliation với tiến độ #65/#67.

Không dùng generic audit events hoặc progress state để lấp event source cho tới khi domain owner xác nhận.

## Kết quả macro-review #65–#67

- #65 đếm progress của learner trong roster; #66 chỉ đếm learning event theo định nghĩa/source được duyệt; #67 trả current lesson state của Student được chọn. `students_with_learning_events` không phải enrollment count và `last_activity_at` không được lấy từ `lesson_progress.last_accessed_at` nếu chưa có domain mapping.
- #65/#67 dùng cùng candidate PUBLISHED lesson set và formula; cả hai vẫn cần duyệt status, duplicate-row, missing-row, rounding và empty rules.
- Tất cả direct response vẫn `Page<Course>` và thiếu request pagination inputs; không tự đổi contract.
- Shared Mentor scope, live schema, error envelope `{}`/`null` và middleware allowlist còn cần xử lý trước implementation.

