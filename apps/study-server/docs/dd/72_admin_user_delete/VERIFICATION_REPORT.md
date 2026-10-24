# Báo cáo kiểm chứng — API #72

- DD status: Draft — Needs Confirmation.
- Endpoint: `DELETE /api/v1/admin/users/{user_id}`.
- Runtime status: `UNWIRED / NOT_FOUND` — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer JWT/Admin, path `user_id:int64!`, `ApiEnvelope<DeleteResult>`, HTTP 200 `DESIGN_RESOURCE_DELETED`; direct errors 401/403/404/422/500.
- DeleteResult direct fields: `id:int64`, status literal `deleted`, `deleted_at:date-time`. Timestamp persistence source chưa xác định.
- Delete policy: diagram yêu cầu soft-delete/anonymize theo policy; không có nguồn cho physical field/table/dependency branch. Không đề xuất hard delete.
- Application tests: `NOT_RUN` — docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; đã đọc đầy đủ cả ba. | PASS |
| Plan trước khi tạo DD | Requirement/request/query/mutation/response-source matrices có trong worklog trước khi tạo folder DD. | PASS |
| Catalog và diagram | API #72 row, DeleteResult, AC-31 index và toàn bộ nodes/edges đã đối chiếu. | PASS — STATIC |
| Source/Admin/auth | Không có route/module/test API #72; shared guard chỉ cho Student; middleware path chưa allowlist. | PASS — STATIC SOURCE REVIEW |
| Schema/dependencies | Legacy users thiếu deletion timestamp và có các FK user-linked; V1-PILOT UUID model được tách; live schema không xác minh. | PASS — STATIC |
| Contract/error | Method/path/auth/path/response/status/error set giữ đúng catalog; không thêm code/status. | PASS |
| Response fields | id/status/deleted_at được liệt kê; deleted_at không gán nguồn vật lý chưa được duyệt. | PASS |
| Policy/data safety | Không có hard-delete/cascade hoặc relation-block rule tự suy ra; response không trả PII. | PASS |
| Template/package | Exact 11-file package; 8/8 appendix suffixes khớp registered templates. | PASS |
| Markdown/JSON/links | JSON parse; relative links/anchors, tables/fences, Unicode và whitespace kiểm tra. | PASS — STATIC |
| AC-31 macro-review | #68–#72 được rà document-level; findings và open gaps đã cập nhật ở các DD liên quan. | VERIFIED_WITH_OPEN_QUESTIONS |
| Application tests | Không chạy; docs-only. | NOT_RUN |
| Context validator | Không áp dụng nếu không sửa context page/manifest. | NOT_APPLICABLE |

## AC-31 group macro-review

Status: `VERIFIED_WITH_OPEN_QUESTIONS` — document-level review of APIs #68–#72.

- #68 list giữ đúng catalog response hiện tại, nhưng catalog khai báo `ApiEnvelope<UserProfile>` trong khi diagram yêu cầu danh sách/pagination; contract cardinality cần được chốt.
- #69 detail và #68 list cùng cần quyết định projection `UserProfile`, visibility của user đã xóa/ẩn danh, PII và audit access.
- #70 PUT profile, #71 PATCH status/session effect và #72 DELETE lifecycle được giữ thành ba thao tác riêng; enum, nullability, trạng thái hợp lệ và tác động session vẫn cần nguồn được duyệt.
- #72 chỉ có logical intent soft-delete/anonymize theo policy. Physical target, dependency rules, `deleted_at` persistence, idempotency và retention chưa được xác định; không suy ra hard delete/cascade từ legacy DDL.
- Cross-cutting: Admin guard chưa có trong Study source; legacy BIGINT `users` và V1-PILOT UUID model không được ghép ngầm; live schema và error-envelope `data` convention chưa được xác minh.
- Runtime status của #68–#72: `UNWIRED / NOT_FOUND`; không có route/module/focused tests cho nhóm. Không chạy application tests trong task docs-only.

## Giới hạn kết luận

Static verification chứng minh cấu trúc và tài liệu nhất quán với contract/diagram đã kiểm tra; không chứng minh API, Admin auth, live schema, persistence, deletion policy hoặc runtime response đã được triển khai.
