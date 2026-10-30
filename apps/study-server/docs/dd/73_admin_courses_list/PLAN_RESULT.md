# Kết quả plan — API #73

## Phạm vi ban đầu

Tạo DD Markdown cho `GET /api/v1/admin/courses` theo catalog và AC-32. Study workflow yêu cầu Markdown và không tạo ZIP.

## Plan đã thực hiện

| Bước | Kết quả |
|---|---|
| Phân loại | `docs`; `server-study`; không có cross-scope dependency. |
| Worklog preflight | Deno selector chọn #48/#49/#50; đọc đầy đủ cả ba trước khi inspect sâu. |
| Diagram/catalog | Đọc API #73 và reusable Course/Page/PageMeta; parse toàn bộ nodes/edges AC-32; chuỗi list → detail → update/status/delete → reload được giữ. |
| Source/schema | Không có route/module/test #73; đối chiếu API #06 source/tests, Admin list #68, legacy DDL, V1-PILOT và category gap. |
| Plan-before-authoring | Requirement, Request Usage, Query, Mutation, Response Source matrices được ghi trong worklog trước khi tạo folder DD. |
| Authoring | Tạo 8 template sheets và 3 reports; proposal được phân biệt khỏi contract trực tiếp. |
| Group review | Đã macro-review #73–#77 sau khi tạo DD #77; cập nhật open questions, plans và verification reports liên quan. |

## Implementation update — 2026-10-26

- Added local route, Admin module, SQL-only query constants, raw-query validation, shared `Page<Course>` response and focused HTTP/OpenAPI tests.
- Uses the shared JWT `ADMIN` guard before query parsing/DB. AC-32's separate course-management permission remains unchecked and is recorded as `DERIVED`/open.
- Legacy `courses/users` is a candidate runtime target. Count/list share exact optional status/mentor predicates, use `id ASC`, page 1/size 20, and no writes. Live schema remains unverified.
- Valid category int64 returns 422 before DB using the API #06 precedent because no physical relation is source-backed. This is a `DERIVED` fallback that differs from the declared category filter.
- Current response errors use `data:null`; the route is registered in `DESIGN_CONTRACT_PATHS`.
- Focused API #73 suite (24 passed), linked #06/#68/#73 regression (60 passed) and full Study suite (830 passed). Ruff and `git diff --check` pass. OpenAPI introspection confirms 41 `/api/v1` paths and 44 operations. DD static checks pass with all 8 template appendices byte-matching. Context validator was attempted with the required Node command and Deno fallback; it remains blocked by baseline missing DB Admin context/source paths and an unavailable registered source commit, outside this task's scope.

## Quyết định tài liệu

- Giữ nguyên response direct `ApiEnvelope<Page<Course>>` và errors 401/403/422/500.
- Page default 1, fixed size 20, `id ASC`, empty list 200, exact-match filters và không default `PUBLISHED` là proposal `DERIVED` dựa trên API #06/#68 và Admin management intent.
- `category` là query field direct nhưng physical relation chưa có nguồn; không tạo `category_id`, bảng nối hoặc JOIN. Runtime hiện trả 422 trước DB theo fallback `DERIVED`.
- Legacy BIGINT `courses/users` chỉ là query candidate; V1-PILOT UUID/versioned course model và live schema được tách.
- Map Course fields theo schema; Course.category optional được omit cho đến khi có source; không trả mentor PII ngoài UserSummary.
- Mentor missing/price invalid đề xuất safe 500 theo API #06; Admin recovery behavior vẫn cần owner xác nhận.
- `07_table.md` là N/A — READ-ONLY API.

## Trạng thái

Draft — Needs Confirmation. API #73 được implement và test cục bộ, nhưng category filter, permission riêng, live schema, enum/casing và orphan recovery vẫn cần owner/schema xác nhận. AC-32 macro-review hoàn tất ở mức tài liệu; implementation #73 không mở rộng runtime #74–#77.
## Kết quả macro-review AC-32

#73 list giữ `Page<Course>`; filter category chưa có relation nguồn nên local fallback 422. Nếu #77 soft-delete thành công, ẩn khỏi list là đề xuất nhất quán nhưng predicate vật lý chưa được chốt. Các API #74–#76 giữ wrapper đúng catalog; #77 dùng `DeleteResult`. Dedicated permission, CourseStatus casing, counters, schema lựa chọn và visibility còn mở; #73 route/error middleware được wire local.
