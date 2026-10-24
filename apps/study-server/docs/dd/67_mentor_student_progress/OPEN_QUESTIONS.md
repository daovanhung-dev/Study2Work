# OPEN_QUESTIONS — Study API #67

Status: Draft — Needs Confirmation. Các câu hỏi cần được chốt trước khi biến candidate thành implementation contract.

1. **Response contract:** Catalog trả `Page<Course>`, còn AC-26 cần progress của một Student. Có sửa sang `StudentCourseProgress` không?
2. **Progress scope:** #67 chỉ chi tiết lesson progress như candidate #65, hay cần gồm quiz/assignment như flow Student AC-18/API #37?
3. **Enrollment eligibility:** Student phải có enrollment trạng thái nào để xuất hiện ở #65 và được xem ở #67? Có gồm completed/withdrawn/hidden account không?
4. **Mentor authorization:** JWT principal ánh xạ tới Mentor ID nào? Quyền dựa trên owner, assignment hay cả hai? Cần cùng rule với các API AC-26.
5. **403/404 privacy:** Course không tồn tại/ngoài scope và Student không tồn tại/không thuộc course được phân biệt thế nào?
6. **Canonical schema:** Dùng legacy BIGINT hay V1-PILOT UUID? API path là int64 nhưng V1-PILOT progress facts dùng enrollment/lesson UUID.
7. **Progress uniqueness:** Legacy DDL không có unique `(user_id, lesson_id)`. Nếu có nhiều row thì chọn current state nào hoặc cần constraint nào?
8. **Lesson denominator:** Có dùng đúng tập lesson PUBLISHED và thứ tự của API #9 như candidate #65/#67 không?
9. **Status/missing row:** Enum progress đầy đủ là gì? Không có progress row có được coi là NOT_STARTED/0 không?
10. **Formula:** Chấp nhận `floor(sum(progress_percent)/total_published_lessons)` và zero khi denominator rỗng để #65/#67 thống nhất không?
11. **Pagination/size:** Candidate trả toàn bộ lesson detail trong một response vì không có page/size input. Có giới hạn course hoặc cần đổi request/response contract không?
12. **Student projection:** Có được trả `full_name` và `avatar_url` theo UserSummary cho Mentor không? Null/omit policy nào áp dụng?
13. **Freshness:** Đọc trực tiếp current state hay dùng snapshot/cache? Nếu dùng snapshot thì freshness/version nào được đảm bảo?
14. **Error envelope:** Khi wire route, đồng bộ API guideline `data:null`, response helper hiện `{}`, và middleware design-code allowlist như thế nào?

## Macro-review AC-26 #65–#67

- Review hoàn tất ở mức tài liệu sau khi DD #67 được tạo; xem [VERIFICATION_REPORT](./VERIFICATION_REPORT.md).
- Ranh giới candidate: #65 class roster summary; #66 course-wide learning-event aggregate; #67 lesson-level current progress của Student được chọn.
- Ranh giới này không sửa contract catalog. Cả ba contract response `Page<Course>` vẫn lệch mục đích AC-26 và request không có pagination inputs.
- #65/#67 dùng chung candidate PUBLISHED lesson denominator và formula; #66 không dùng lesson_progress hoặc snapshot thay learning events.
- Authorization, enrollment eligibility, ID/schema model, formula approval và error policy vẫn là open questions.
