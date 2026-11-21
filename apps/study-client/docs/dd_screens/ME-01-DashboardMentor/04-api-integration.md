# ME-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ME-01-API-001` | #46 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-01-API-002` | #54 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ME-01-API-003` | #58 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #46, #54, #58
- Orchestration/data notes: GET #46/#54/#58 theo quyền; mỗi widget có trạng thái lỗi độc lập.
- BE/source status và gate: **D**; **BLOCK:** Role introspection Mentor chưa có
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 6. Đặc tả API và mapping

### API #46 — Mentor-owned courses

| Thuộc tính | Current source |
|---|---|
| Method / endpoint | `GET /api/v1/mentor/courses` |
| Auth | `Authorization: Bearer <access JWT>`; role `MENTOR`; owner lấy từ numeric JWT `sub` |
| Query | `status?` enum `DRAFT`/`PUBLISHED`; `page=1`; `size=20`, range `1..100`. Dashboard không có course filter. |
| Query/effect | Đếm rồi list `courses` theo `c.mentor_id=:mentor_id`, LEFT JOIN mentor user; order `created_at DESC, id ASC`; read-only. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `data.items[]`, `data.pagination{page,size,total,total_pages}`. Course fields: `id`, `title`, `description?`, `thumbnail_url?`, `price` decimal string, `status`, `mentor{id,full_name,avatar_url?}`. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. Empty/out-of-range page là 200; `total_pages=0` khi total=0. |
| Limitation | Course “assigned” không được query; không có enrollment/progress/course-rating/count fields. API source hiện tại chưa xác minh database live. |

### API #54 — Mentor submissions list

| Thuộc tính | Current source |
|---|---|
| Method / endpoint | `GET /api/v1/mentor/submissions` |
| Auth | Bearer access JWT; role `MENTOR`; owner lấy từ numeric JWT `sub` |
| Query | `course_id?` int64 dương; `status?` exact string, không enum validation; `page=1` positive int32. Page size là 20 cố định; không gửi `size`. |
| Query/effect | Count/list qua `assignment_submissions` → `assignments` → `courses` → `users`; giới hạn `courses.mentor_id`; order `submitted_at DESC, id DESC`. Có course filter thì truy vấn course khác owner trả 403. LEFT LATERAL lookup upload candidate theo exact URL, student owner, `SUBMISSION` purpose, course. Read-only. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `data.items[]`, `data.pagination{page,size=20,total,total_pages}`. Fields: `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?` (decimal string), `feedback?`. `files[]` current mapper tối đa 1 UploadAsset. |
| Errors | 401 authentication; 403 role/other-owner course; 422 validation; 500 internal/mapping. Empty hoặc course filter không tìm thấy là 200 với trang rỗng; 409 còn trong catalog snapshot nhưng source không có current trigger. |
| Limitation | Status string không define “pending”; response không có Student summary, assignment/course title, deadline, rubric hoặc overdue policy. Assignment/upload relation là derived; test dùng fake DB, live schema chưa xác minh. |

### API #58 — Mentor support requests

| Thuộc tính | Current source |
|---|---|
| Method / endpoint | `GET /api/v1/mentor/support/requests` |
| Auth | Bearer access JWT; role `MENTOR`; owner lấy từ numeric JWT `sub` |
| Query | `course_id?` int64 dương; `status?` exact string; không pagination. Nếu course filter thuộc Mentor khác thì trả 403. |
| Query/effect | List requests theo `courses.mentor_id`; khi có rows, list toàn bộ thread/assets trong owner scope. Request order `created_at DESC,id DESC`; messages `created_at ASC,id ASC`; assets theo `asset_position`. Read-only; không gọi thread query khi collection rỗng. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `data` là `SupportRequest[]`. Mỗi record có `id`, `course_id`, `student{id,full_name,avatar_url?}`, `status`, `messages[]`, `created_at`, `resolved_at?`; mỗi message có `id`, author summary, content, attachments, created_at. Empty là `[]`. |
| Errors | 401 authentication; 403 role/other-owner course; 422 invalid `course_id`; 500 query/projection failure. Course filter không tìm thấy trả `[]`/200. |
| Limitation | Không có pagination/summary/subject/unread/SLA/course title/last-message timestamp. Response chứa full message threads; support tables, lifecycle and attachment mapping are derived from checked-in migration 008. Live schema/deployment chưa xác minh. |

**Envelope:** ba API hiện dùng standard envelope `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; API #46/#54 `data` chứa page; #58 `data` là array. Không chuyển #58 thành `Page<SupportRequest>` hoặc response khác dựa trên mockup.

### Trích từ DD nguồn: 13. Nguồn truy vết

- [Inventory/F08/F09/API index](../../list_screen.md), [global plan](../../screen_stitch/dd_screens/PLAN.md), [AC-03 Mentor Teaching](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio).
- [Current Study router](../../../../study-server/app/api/v1.py), [API #46 view](../../../../study-server/app/modules/mentor/api_46_mentor_courses/view.py), [#46 query/model/validator](../../../../study-server/app/modules/mentor/api_46_mentor_courses), [#54 view](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list/view.py), [#54 model/query](../../../../study-server/app/modules/mentor/api_54_mentor_submissions_list), [#58 view](../../../../study-server/app/modules/mentor/api_58_mentor_support_requests/view.py), [#58 model/query](../../../../study-server/app/modules/mentor/api_58_mentor_support_requests), [shared Mentor auth guard](../../../../study-server/app/utils/auth.py).
- [#46 tests](../../../../study-server/tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py), [#54 tests](../../../../study-server/tests/modules/mentor/api_54_mentor_submissions_list/test_mentor_submissions_list.py), [#58 tests](../../../../study-server/tests/modules/mentor/api_58_mentor_support_requests/test_mentor_support_requests.py) — source inspected, not executed here; tests use fake database projections.
- [API #46 DD snapshot](../../../../study-server/docs/dd/46_mentor_courses/02_Overview.md), [#54 DD snapshot](../../../../study-server/docs/dd/54_mentor_submissions_list/02_Overview.md), [#58 DD snapshot](../../../../study-server/docs/dd/58_mentor_support_requests/02_Overview.md): `Draft — Needs Confirmation`, secondary to current source.
- [Server module index and current notes](../../../../../.agents/server-study/modules/README.md), [DB evidence](../../../../../.agents/server-study/database.md), [Study Web status](../../../../../.agents/web-work/study/INDEX.md), [Study Web design target](../../../../../.agents/web-study/design.md), [cross-scope dependency](../../../../../.agents/project/dependencies.md), [API guidelines](../../../../../contracts/api-guidelines/README.md).

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md)
