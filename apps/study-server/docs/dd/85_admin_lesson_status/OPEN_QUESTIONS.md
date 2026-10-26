# Câu hỏi còn mở — API #85

Trạng thái: `Draft — Needs Confirmation`. Runtime đã chọn fallback DERIVED để có implementation nhất quán; các mục sau cần owner/schema confirmation trước khi coi là contract được duyệt hoặc triển khai production.

1. **Status enum:** Implementation dùng `DRAFT`, `PUBLISHED`, `SUSPENDED` theo API #76 vì lesson-specific enum chưa có nguồn. Owner có xác nhận dùng chung tập này cho Lesson không?
2. **Transition policy:** Hiện không có transition matrix, readiness, moderation, enrollment hoặc progress condition. Có cần bổ sung rule nào không?
3. **Same status và retry:** Implementation coi cùng status là no-op và không tạo audit duplicate; không có idempotency key. Xác nhận chính sách này.
4. **Audit schema/deployment:** Migration 012 tạo `lesson_status_audit_logs` theo legacy BIGINT Lesson. Xác nhận runtime/live DB dùng schema legacy và migration đã được áp dụng trước deploy.
5. **Audit semantics:** Hiện lưu actor, lesson ID, status cũ/mới, timestamp; không có reason/trace field. Xác nhận đủ dữ liệu audit.
6. **Admin authorization:** Current guard yêu cầu role `ADMIN`; AC-34 còn nêu lesson-management permission riêng. Xác nhận policy/claim để thực thi permission đó.
7. **Timestamp:** Implementation cập nhật `lessons.updated_at` bằng `CURRENT_TIMESTAMP`; xác nhận không có DB trigger/owner khác.
8. **404/soft delete:** #85 trả 404 khi row không tồn tại, chưa lọc soft-delete marker. Đồng bộ policy visibility với API #82–#84 và #86.
9. **Lesson projection:** Reusable Lesson yêu cầu `course_id:int64`, trong khi legacy DDL cho phép NULL. Xác nhận dữ liệu thực tế không tạo projection lỗi 500.
10. **Validation/envelope:** Local body enum/422 shape và `data:null` error envelope đã được HTTP-test; xác nhận giữ làm API contract.

## Decision record

- DIRECT: method/path/Bearer/Admin/path type/response/error set; AC-34 yêu cầu status + audit rồi reload list.
- DERIVED: body `{status}`, enum ba giá trị, legacy BIGINT audit table migration 012, row lock, updated timestamp, same-status no-op và transaction rollback behavior.
- SOURCE_REQUIRED before production claim: live schema/migration deployment, fine-grained permission, soft-delete policy, Lesson nullability and owner approval of status rules.
