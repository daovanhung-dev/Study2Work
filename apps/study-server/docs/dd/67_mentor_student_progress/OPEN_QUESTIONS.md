# OPEN_QUESTIONS — Study API #67

Status: Draft — Needs Confirmation. Runtime dùng fallback DERIVED dưới đây; business/contract owner cần phê duyệt hoặc thay đổi trước khi coi đây là contract chuẩn.

1. **Response contract:** Diagram/catalog ghi `Page<Course>`, runtime theo mục tiêu AC-26 đang trả singular `StudentCourseProgress`. Có phê duyệt đổi response chuẩn và đồng bộ catalog/diagram không?
2. **Progress scope:** Runtime chỉ chi tiết lesson progress như nhóm #65, hay cần gồm quiz/assignment như flow Student AC-18/API #37?
3. **Enrollment eligibility:** Runtime dùng `enrollments.status='ACTIVE'` và `users.role='STUDENT'` như #65. Có bao gồm completed/withdrawn/hidden account theo policy khác không?
4. **Mentor authorization:** Runtime dùng JWT numeric `sub` khớp `courses.mentor_id`; cần hỗ trợ Mentor assignment ngoài direct ownership không?
5. **403/404 privacy:** Runtime trả 403 cho course của owner khác và 404 khi course/Student không nằm trong scope. Privacy policy chuẩn có cùng thứ tự không?
6. **Canonical schema:** Live deployment dùng legacy BIGINT hay V1-PILOT UUID? API path là int64 nhưng pilot progress facts dùng enrollment/lesson UUID.
7. **Progress uniqueness:** Legacy DDL không có unique `(user_id, lesson_id)`. Runtime chọn latest `last_accessed_at DESC NULLS LAST, id DESC` như #65; có cần canonical uniqueness/selection rule khác không?
8. **Lesson denominator/order:** Có phê duyệt cùng PUBLISHED lesson set và `sort_order,id` của #9/#65 không?
9. **Status/missing row:** Runtime cho phép `NOT_STARTED|IN_PROGRESS|COMPLETED`; absent row thành NOT_STARTED/0. Đây có phải state machine và default chuẩn không?
10. **Formula:** Có phê duyệt `floor(sum(progress_percent)/total_published_lessons)` và zero khi denominator rỗng để #65/#67 thống nhất không?
11. **Pagination/size:** Request không có page/size nên runtime trả tất cả lesson detail. Cần giới hạn course hoặc đổi request/response contract không?
12. **Student projection:** Runtime trả `id`, `full_name`, `avatar_url` và giữ avatar null trong JSON. Projection/privacy/null policy này có được duyệt không?
13. **Freshness:** Runtime đọc current `lesson_progress` rows; không dùng snapshot/cache. Có yêu cầu freshness/version khác không?

## Macro-review AC-26 #65–#67

- Review AC-26 và implementation hoàn tất ở mức source/test cục bộ; xem [VERIFICATION_REPORT](./VERIFICATION_REPORT.md).
- Ranh giới runtime: #65 class roster summary; #66 course-wide learning-activity proxy; #67 lesson-level current progress của Student được chọn.
- Diagram/catalog vẫn khai báo `Page<Course>` cho cả ba API, khác với dữ liệu AC-26 cần; API #67 đã wire với singular DERIVED fallback.
- #65/#67 dùng chung PUBLISHED lesson denominator, latest-progress rule và floor-average formula; #66 không dùng `lesson_progress` thay learning-event history.
- Shared Mentor guard và error helper hiện là source facts; direct-owner mapping, enrollment/business approval, schema, formula/duplicate approval và pagination vẫn là open questions.
