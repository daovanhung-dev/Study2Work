# Báo cáo kiểm chứng — API #76

- DD status: Draft — Needs Confirmation.
- Endpoint: PATCH /api/v1/admin/courses/{course_id}/status.
- Runtime status: UNWIRED / NOT_FOUND — route, module, Admin guard và focused test không có trong Study source.
- Direct contract: Bearer/Admin; path course_id:int64!; body chưa khai báo; ApiEnvelope&lt;Page&lt;Course&gt;&gt;; HTTP 200 DESIGN_RESOURCE_UPDATED; errors đúng 401/403/404/422/500 theo catalog.
- Derived proposal: body {status}, target DRAFT/PUBLISHED/SUSPENDED, legacy courses.status update, updated_at, atomic audit/write transaction và response Page singleton.
- Source gaps: physical audit mapping không tương thích/được chọn; Admin guard, live schema, transition/readiness/no-op and idempotency behavior unresolved.
- Application tests: NOT_RUN — docs-only.

## Kiểm tra

| Check | Kết quả | Trạng thái |
|---|---|---|
| Worklog preflight | Selector chọn #48/#49/#50; cả ba đã đọc đầy đủ. | PASS |
| Plan trước folder | Requirement, Request Usage, Query, Mutation, Response Source matrices có trong worklog trước authoring. | PASS |
| Catalog/diagram | API #76 exact row, reusable schemas, AC-32 index và toàn bộ node/edge đã đối chiếu. | PASS — STATIC |
| Current source/schema | Xác nhận chưa có route/module/test; đã đối chiếu Student-only guard, middleware allowlist và legacy/pilot schema split. | PASS — STATIC; endpoint vẫn UNWIRED |
| Contract/error | Method/path/auth/path, response, success và đúng năm error code catalog. | PASS — STATIC |
| Field/mutation coverage | Đủ Course/UserSummary/Page fields; status update và logical audit intent có mapping/gap riêng. | PASS_WITH_OPEN_QUESTIONS |
| Template/package | Đủ đúng 11 file; front matter có mặt và appendix suffix 8/8 byte-match template đã đăng ký. | PASS — STATIC |
| Markdown/JSON/links | 2 JSON examples parse; 32 bảng, 8 code fences, 26 local links và 10 anchors kiểm tra được; newline/whitespace sạch. | PASS — STATIC |
| Cross-matrix consistency | Request/body, Q1/M1/M2/Q2, response và error branches đối chiếu; phần suy dẫn/source-required vẫn được gắn nhãn. | PASS_WITH_OPEN_QUESTIONS |
| AC-32 macro-review | Đã rà #73–#77; giữ đúng ranh giới metadata/status+audit/soft-delete, các policy và schema gaps còn mở. | COMPLETED_WITH_OPEN_QUESTIONS |
| Application tests | Not run; docs-only. | NOT_RUN |
| Context validator | No context page/registry modified. | NOT_APPLICABLE |

## Giới hạn kết luận

Static DD verification only shows consistency with current catalog, diagram, source artifacts and documented candidates. It does not prove the Admin endpoint, audit persistence, live schema or runtime behavior.

## Fingerprints

| Fingerprint | Phạm vi | SHA-256 |
|---|---|---|
| Registered template pack | 8 template sheets; sorted filename + NUL + raw file bytes + NUL | `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137` |
| DD output payload | 8 sheets + `OPEN_QUESTIONS.md` + `PLAN_RESULT.md`; excludes this report; same hash algorithm | `9ffb9af4a6a06b41fb4ca58a73f7a0325e9ae35c7f026ec311c024fa4c8a2457` |
## Kết quả macro-review AC-32 #73–#77

- Ownership/side effects nhất quán: #73 list, #74 detail, #75 metadata-only, #76 status + audit intent, #77 soft-delete theo policy. #73–#76 giữ `Page<Course>` đúng catalog; #77 dùng `DeleteResult`.
- Không đưa CourseStatus vào #75; không chuyển status/audit sang #77; không thực hiện hard-delete/cascade. Các body/mutation chưa có trong catalog tiếp tục được đánh dấu proposal.
- Status visibility, deleted-target behavior, audit persistence, enrollment/content dependency policy, physical marker/timestamp, Admin guard, live schema, error envelope và dynamic path middleware vẫn cần quyết định.
- Macro-review là static document review; không chứng minh runtime/live schema và không chạy application tests.
