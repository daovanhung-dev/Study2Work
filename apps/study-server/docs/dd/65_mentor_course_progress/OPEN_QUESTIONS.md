# Open Questions — Study API #65

Status: Draft — Needs Confirmation. Các câu hỏi dưới đây cần được chốt trước khi implementation-ready.

1. **Response contract:** Catalog trả Page<Course>, còn AC-26 cần learner/progress. Có sửa catalog sang Page<MentorStudentProgress> không? Candidate này là DERIVED, chưa được duyệt.
2. **Pagination:** Có thêm page/size không? Nếu không, chấp nhận một roster page không giới hạn hay đặt giới hạn/giải pháp khác?
3. **Mentor identity/access:** JWT principal map tới Mentor/user ID nào? Có hỗ trợ Mentor được assign course không? Thứ tự 403/404 theo privacy policy là gì?
4. **Enrollment set:** Lọc enrollment theo status nào? Có loại duplicate, withdrawn, deleted hoặc non-Student user không?
5. **Lesson denominator:** Tính tất cả lesson hay chỉ PUBLISHED? API #9 public curriculum gợi ý PUBLISHED, nhưng AC-26 không nói rõ.
6. **Progress formula:** completed_lessons, phần trăm, rounding và missing progress row được tính thế nào? Status enum chính xác là gì? Candidate floor(sum(percent)/total_lessons) chỉ là DERIVED.
7. **Schema:** Dùng schema live nào? Legacy BIGINT DDL và V1-PILOT UUID/versioned DDL không khớp nhau; chưa có live metadata proof.
8. **Consistency/freshness:** Progress lấy trực tiếp từ facts hay snapshot/cache? Có freshness/SLA hay snapshot timestamp không?
9. **Error envelope:** Khi triển khai, thống nhất guideline data:null với helper hiện trả {} cho absent data; xác nhận middleware allowlist cho path mới.
10. **Empty class/course:** Có trả page rỗng khi không có learner/lesson không? Metadata size/total_pages cụ thể ra sao?

Không tự quyết định các câu hỏi này bằng suy đoán trong DD. Contract catalog direct vẫn là Page<Course> cho tới khi owner phê duyệt thay đổi.

## Macro-review AC-26 after DD #67

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`; see [API #67 verification report](../67_mentor_student_progress/VERIFICATION_REPORT.md).
- #65 stays class-level roster summary; #66 stays course-wide event analytics; #67 is selected-Student lesson progress detail. The diagram sequence is UI orchestration, not server-to-server coupling.
- #65 and #67 proposals share PUBLISHED lesson denominator and floor-average formula. #66 event-active Student count is distinct from #65 enrollment count; progress state/time fields are not event source.
- Open: `Page<Course>` mismatch and missing page/size inputs in all three; shared Mentor course-scope identity/assignment/privacy policy; selected live schema; enrollment eligibility; duplicate progress rows; formula/status/empty semantics; error envelope and middleware path mapping.

