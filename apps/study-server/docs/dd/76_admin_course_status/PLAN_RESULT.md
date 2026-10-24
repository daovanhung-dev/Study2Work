# Kết quả plan — API #76

## Phạm vi

Tạo Markdown DD cho PATCH /api/v1/admin/courses/{course_id}/status theo API catalog và AC-32. Chỉ tạo tài liệu #76; không sửa source, DB, schema, migration, catalog hoặc diagram. Study workflow yêu cầu folder Markdown, không tạo ZIP.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại | docs; scope server-study; không có cross-scope dependency. |
| Worklog preflight | Deno selector chọn #48/#49/#50; đọc đủ cả ba trước khi inspect sâu. |
| Context/skill/template | Router/context-map/scope/API workflow đọc; manifest xác nhận createDD-markdown/docs-dd; 8 template Markdown được dùng, appendix baseline được giữ. |
| Catalog | Giữ method/path, Bearer/Admin, path int64, Page&lt;Course&gt;, 200 update và đúng 401/403/404/422/500; body trực tiếp chưa khai báo. |
| AC-32 | Parse toàn bộ nodes/edges; STATUS branch là API #76 → update status + audit log → reload management. |
| Prior DD | #71 body status là precedent DERIVED; #73–#75 giữ status tách khỏi metadata; #74/#75 singleton Page là response precedent. |
| Current source | API #76 chưa route/module/test; current auth Student-only; Admin path chưa nằm trong middleware design-code allowlist. |
| Schema | Legacy BIGINT courses.status candidate; V1-PILOT UUID/versioned status/audit schema khác và không tương thích trực tiếp; live schema chưa xác minh. |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation và Response Source matrices được ghi trong worklog trước khi tạo DD folder. |
| Authoring | Tạo 8 template sheets + 3 reports; field/body/mutation proposals phân biệt DIRECT/DERIVED/SOURCE_REQUIRED. |
| Macro-review | Đã rà nhóm #73–#77 sau khi #77 tồn tại; giữ ranh giới status/audit tách khỏi metadata/delete. |

## Quyết định tài liệu

- Giữ nguyên catalog response ApiEnvelope&lt;Page&lt;Course&gt;&gt;, HTTP 200 DESIGN_RESOURCE_UPDATED và đúng error set; không thêm 409.
- Body {status:CourseStatus!} là DERIVED vì catalog/diagram không khai báo body trong khi thao tác cần trạng thái đích.
- Semantic values draft/published/suspended theo catalog; candidate uppercase DRAFT/PUBLISHED/SUSPENDED dựa legacy/current #06 convention. Exact enum/casing cần approval.
- Transition matrix/no-op/readiness không có trong AC-32; DD đề xuất target assignment cho một status thuộc candidate set và để policy còn lại mở.
- Diagram bắt buộc audit event. Legacy DB không có audit relation; pilot audit_events dùng UUID khác API int64. DD không bịa physical INSERT; đánh dấu SOURCE_REQUIRED và coi atomic status+audit là proposal.
- Course status update dùng legacy BIGINT columns chỉ làm candidate; V1-PILOT và live schema giữ tách biệt.
- Response Page singleton theo #74/#75; map Course + UserSummary, omit optional category khi thiếu relation.
- Admin guard, response pagination convention, Idempotency-Key, error data:null và middleware allowlist cần owner/runtime integration.

## Trạng thái

Draft — Needs Confirmation. DD chưa implementation-ready do body/status enum, Admin authorization, physical audit persistence, live schema, state transitions, projection nullability và retry semantics chưa được xác nhận.
## Kết quả macro-review AC-32 — 2026-10-24

#76 chỉ sở hữu status update và audit intent trong nhánh diagram; không áp audit cho #77 theo suy đoán. #75 metadata-only, #77 soft-delete-only. Status visibility và cách các API xử lý soft-deleted target cần thống nhất sau khi policy/marker được chốt; Admin guard, schema và error integration vẫn là blockers.
