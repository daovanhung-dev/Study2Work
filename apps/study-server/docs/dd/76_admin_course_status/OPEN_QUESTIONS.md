# Câu hỏi còn mở — API #76

Trạng thái tài liệu: Draft — Needs Confirmation. API #76 hiện có implementation local dựa trên các fallback `DERIVED` dưới đây; tài liệu này không thay cho phê duyệt owner hoặc xác minh schema/deployment.

1. **Body contract:** Runtime local dùng `application/json` `{ "status": "DRAFT|PUBLISHED|SUSPENDED" }`, strict/extra-forbid. Catalog và diagram không khai báo body; owner cần duyệt fallback này.
2. **CourseStatus enum/casing:** Runtime dùng uppercase `DRAFT`, `PUBLISHED`, `SUSPENDED` theo catalog semantic labels và legacy/current convention. Reusable CourseStatus không liệt kê members; owner cần chốt enum.
3. **Transition/readiness:** Local fallback cho phép đặt trực tiếp một target status trong allowlist, không có readiness gate. Owner cần xác nhận policy publish/reopen/suspend.
4. **Same-status/retry:** Local same-status request là no-op, không đổi `updated_at` hoặc ghi audit duplicate. Catalog không định nghĩa idempotency header; xác nhận nếu cần request-key semantics.
5. **Suspension access:** Public course listing/detail gates `PUBLISHED`; quyền tiếp tục truy cập lesson của learner đã enroll khi course bị SUSPENDED chưa rõ. Không có enrollment/content side effect.
6. **Audit schema:** Local fallback thêm `course_status_audit_logs` (BIGINT course/admin FKs, previous/new status, changed_at), migration 010 và write cùng transaction. Đây là `DERIVED`, không phải schema được owner duyệt; retention, DB-enforced append-only/integrity và live application chưa xác minh.
7. **Live schema:** Code nhắm legacy BIGINT `courses/users`; không nhắm V1-PILOT UUID `course_versions/audit_events`. Chưa có bằng chứng migration/live relation đã được áp dụng.
8. **Admin authorization:** Runtime kiểm tra shared JWT role `ADMIN`. Mapping sang AC-32 finer course-management permission, tenant/scope, MFA và current-user-status revocation chưa có policy source.
9. **Response/projection:** Giữ `ApiEnvelope<Page<Course>>` và singleton pagination theo #74/#75. Legacy `mentor_id`/`price` có thể NULL/orphan dù Course contract yêu cầu giá trị; local mapping trả 500 nếu projection không hợp lệ.
10. **Soft delete:** API #77 chưa chốt marker/visibility predicate. #76 không tự thêm deleted-target filter; cần thống nhất sau khi #77 persistence được chọn.

## Ranh giới proposal

- Direct: endpoint/method/path, Admin actor/precondition, semantic status labels, `Page<Course>`, success/error status codes, diagram audit intent.
- DERIVED implementation: JSON body, uppercase status members, shared ADMIN role, legacy BIGINT audit relation/actor mapping, direct target assignment, same-status no-op, singleton Page, atomic transaction.
- SOURCE_REQUIRED/NOT_VERIFIED: finer permission, live DB/migration/deployment, transition/readiness and suspension access policy, retention/DB immutability, nullable/orphan Course policy and idempotency-key requirement.
- Không thêm business code hoặc HTTP status ngoài catalog.

## Macro-review AC-32 #73–#77

#76 giữ status + audit tách khỏi #75 metadata và #77 soft-delete. Không chuyển audit sang #75/#77; không thêm enrollment/content mutation hoặc readiness gate. #73/#74/#75/#76 current source tests đều là local HTTP/source evidence, không xác nhận DB live.
