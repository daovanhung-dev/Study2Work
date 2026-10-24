# Câu hỏi còn mở — API #85

Trạng thái: Draft — Needs Confirmation. Catalog/diagram chỉ khai báo path; request body dưới đây là proposal DERIVED, chưa phải contract được duyệt.

1. **Request body:** Xác nhận body JSON có field bắt buộc status không? Có field nào khác không?
2. **Status enum:** LessonStatus có những giá trị và casing nào? Legacy default DRAFT không phải danh sách enum.
3. **Transition policy:** Trạng thái nào được chuyển sang trạng thái nào? Có readiness, moderation, enrollment hoặc progress condition không?
4. **Same status và retry:** Gửi lại cùng status là no-op hay vẫn tạo audit? Retry có idempotency contract không?
5. **Audit semantics:** Event phải lưu actor, lesson ID, trạng thái cũ/mới, reason, trace hoặc metadata nào?
6. **Audit schema:** Chọn physical relation và mapping nào? Legacy Study DDL không có audit relation; V1-PILOT audit_events dùng UUID trong khi legacy lesson ID là BIGINT.
7. **Active schema:** Runtime dùng legacy BIGINT lessons hay V1-PILOT UUID/versioned model? Live schema/migration state đã được xác nhận chưa?
8. **Timestamp:** Có cập nhật updated_at khi đổi status không? Trigger hay application caller là owner?
9. **Transaction:** Status và audit phải nguyên tử theo AC-34; caller/use case nào sở hữu transaction/commit/rollback?
10. **Admin authorization:** JWT claim nào xác nhận role Admin và lesson-management permission? Principal ID map sang audit actor thế nào?
11. **404/soft delete:** Không có lesson có trả 404 DESIGN_RESOURCE_NOT_FOUND không? Sau policy soft-delete ở #86, xác nhận #82 list, #83 detail và #84/#85 mutation xử lý lesson đó nhất quán thế nào.
12. **422:** Path/body validation conditions và meta.fieldErrors shape nào được duyệt?
13. **Response nullability:** Legacy course_id nullable nhưng reusable Lesson yêu cầu int64; content/video_url null serialize hay omit?
14. **Error envelope:** Guideline yêu cầu data:null; current helper defaults absent data to {}. Quyết định integration behavior khi wire route?
15. **Middleware and tests:** Khi API được implement, Admin route guard/allowlist, matching HTTP tests và runtime verification plan là gì?

## Ranh giới proposal

- DIRECT: method/path/auth/role/path type/response/status/error codes; AC-34 permission and status+audit intent.
- DERIVED: one-field status body, JSON encoding, legacy one-row update/returning, updated_at candidate and no-row 404.
- SOURCE_REQUIRED: enum/transition rules, physical audit mapping, active schema/live DB, Admin policy, transaction owner and error integration.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Audit chỉ thuộc nhánh status #85 theo AC-34; ranh giới mutation và reload được ghi trong [báo cáo macro-review](../86_admin_lesson_delete/VERIFICATION_REPORT.md#ac-34-macro-review).
