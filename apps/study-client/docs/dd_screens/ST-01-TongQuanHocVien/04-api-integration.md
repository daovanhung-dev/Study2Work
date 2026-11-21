# ST-01 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-21

ST-01 independently calls source-backed #20 and #38 through the authenticated
Student client. #20 returns `CourseSummaryPage` with ACTIVE enrollment rows,
page size 20 and enrolled-time descending order; #38 returns the recorded
`AchievementPage` ordered by award time and ID descending. The page validates
their success envelope/business code, page shape and consumed fields, and
offers per-widget retry. For separate COUNT/LIST reads on #20 and #38, the
presentation layer compares returned item count with the count-derived
expected rows for the requested page to avoid false empty copy and offers the
existing retry on mismatch; the shared guards do not impose cardinality
equality. #21 still returns `UserProfile`, and #43 still relies
on `notification_recipients` absent from checked-in DDL, so neither is called.
Focused/runtime verification remains outstanding; detailed design-time
contracts below are preserved as expected behavior.

## Current caller status — 2026-11-17

ST-01 calls #20 for ACTIVE courses and #38 for recorded achievements. It does
not call #21 because the current response is `UserProfile`, not progress, and
does not call #43 because the descriptor is `SOURCE_ONLY` and the query
depends on `notification_recipients`, absent from checked-in DDL. The DD/API
excerpt below preserves the design-time contract; for callers and current
source status see [the screen inventory](../../list_screen.md) and
[T038 gap matrix](../../../../../.agents/worklog/2026-11-17/T038-screen-gap-matrix.md).

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-01-API-001` | #20 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-002` | #21 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-003` | #38 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-01-API-004` | #43 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #20, #21, #38, #43
- Orchestration/data notes: Chỉ sau role STUDENT hợp lệ; load #20/#21; thành tích #38, thông báo #43 lazy/parallel.
- BE/source status và gate (current source 2026-11-20): **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED.** #20 and #38 routes/callers are source-wired and their current projections are checked by ST-01. #20 source returns a paged enrollment/course projection instead of catalog `UserProfile`; #21 route exists but returns `UserProfile`, so it cannot supply progress; #43 remains `SOURCE_ONLY` for this screen because its query depends on `notification_recipients`, absent from checked-in DDL. Award producer/rules, AC-13 empty branch, AC-18 ordering, #43 recipient/order contract and visual fidelity remain open. The no-route/UNWIRED wording in the older source-status excerpt is a historical snapshot, not current behavior.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-01 khai báo `/student`, actor Student, widget khóa học/tiến độ/thành tích/thông báo; #20/#21 khi vào màn hình, #38/#43 lazy hoặc parallel; state labels `partial-widget/empty/loading/403`. Đây là target design, không xác nhận runtime.
- AC-13 yêu cầu #20 đọc danh sách Enrollment/Course, sau đó #21 đọc tiến độ và client ghép theo course. Activity diagram có nhánh `EMPTY` và `HAS DATA` cùng đi tới node “Hiển thị khóa học + % hoàn thành”. Đây là `DISCREPANCY`; không tự sửa nhánh hoặc chọn một order khác.
- AC-18 yêu cầu #21 aggregate, chọn một course, #37 detail progress, #38 achievement rồi render. Inventory ST-01 và ST-20 lại xem #21/#38 là các widget độc lập. Không suy luận thời điểm gọi #38 hoặc ép ST-01 theo chuỗi chi tiết AC-18.
- AC-20 định nghĩa #43 lấy notification list/unread badge; #44/#45 thực hiện mark-read ở luồng notification center. ST-01 chỉ có link tới ST-26, không có mutation event.
- API catalog contract được giữ nguyên: #20 GET `/api/v1/users/me/courses`; #21 GET `/api/v1/users/me/progress`; #38 GET `/api/v1/users/me/achievements`; #43 GET `/api/v1/users/me/notifications`. Không dùng các endpoint path khác xuất hiện trong HTML.
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) là nguồn quy trình; API catalog/DD và current source là các bằng chứng riêng.

### Trích từ DD nguồn: A.4. Ma trận API và source status

| API | Request theo catalog | Response / statuses theo catalog | Current source và điểm chưa chốt |
|---|---|---|---|
| #20 | `GET /api/v1/users/me/courses`; Student Bearer; `status?:string`, `page?:int32`; body không khai báo. | Catalog: `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/422/500. | Current route/view/query/model exist; authenticated owner-scoped `CourseSummaryPage`, fixed page size 20, enrollment-time/ID descending. ST-01 sends `status=ACTIVE&page=1` and validates the page projection. Catalog-vs-source and AC-13 response/empty discrepancies remain. |
| #21 | `GET /api/v1/users/me/progress`; Student Bearer; query ghi `course_id list hoặc aggregate?:string`; body không khai báo. | Catalog: `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/500. | Current route/view/query/model exist but return `UserProfile` only. ST-01 does not call it as it supplies no progress DTO, merge key, formula or aggregate result. Selector, identity and no-progress semantics remain unresolved. |
| #38 | `GET /api/v1/users/me/achievements`; Student Bearer; `course_id?:int64`; body không khai báo. | Catalog: `ApiEnvelope<Page<Achievement>>`; fields `id`, `code`, `title`, `awarded_at`, `course_id?`; 200/401/403/500. | Current route/view/query/model exist; returns recorded owner-scoped achievements ordered by award time and ID descending. ST-01 validates the projection/page. Award producer/rules, filter/access and catalog-vs-source pagination/empty semantics remain open; no contract supports certificate, proof, KPI or signature. |
| #43 | `GET /api/v1/users/me/notifications`; Student Bearer; `unread_only?:boolean`, `page?:int32`; body không khai báo. | Catalog: `ApiEnvelope<Page<Notification>>`; 200/401/403/500. | Source query/module exists and depends on `notification_recipients`, absent from checked-in DDL; client descriptor is not usable by ST-01 (`SOURCE_ONLY`), so no caller is made. Recipient/broadcast, channels/status, read timestamps, ordering, timezone and error-envelope behavior remain unresolved. |

Tài liệu từng API: [#20](../../../../study-server/docs/dd/20_users_me_courses/02_Overview.md) / [questions](../../../../study-server/docs/dd/20_users_me_courses/OPEN_QUESTIONS.md), [#21](../../../../study-server/docs/dd/21_users_me_progress/02_Overview.md) / [questions](../../../../study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md), [#38](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md) / [questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md), [#43](../../../../study-server/docs/dd/43_users_me_notifications/02_Overview.md) / [questions](../../../../study-server/docs/dd/43_users_me_notifications/OPEN_QUESTIONS.md). DDL/ERD là design evidence, không phải live schema proof.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md)
