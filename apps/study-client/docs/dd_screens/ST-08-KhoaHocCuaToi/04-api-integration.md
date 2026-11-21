# ST-08 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## Current caller status — 2026-11-17

ST-08 calls paged API #20 and renders returned course/enrollment fields with
loading, error, empty and pagination states. It does not call #21 because the
current response is `UserProfile`, not progress. The DD/API excerpt below
preserves the design-time contract; for current source/caller status see
[the screen inventory](../../list_screen.md) and [T038 gap matrix](../../../../../.agents/worklog/2026-11-17/T038-screen-gap-matrix.md).

## Current caller status — 2026-11-21

The current page validates #20's success envelope/business code and the
source-backed `CourseSummaryPage` before rendering: requested page, fixed size
20, page metadata, course/enrollment projection and enrolled-time ordering.
The status filter is not exposed by ST-08 and #21 remains unused because it
returns `UserProfile`. The design-time catalog still declares
`ApiEnvelope<UserProfile>` for #20; that response-shape discrepancy remains
open. If the validated response's `total_pages` falls below the requested
page, the page now moves to `max(total_pages, 1)` and repeats the same #20
request before rendering. For accepted pages, the client compares returned
item count with the row count implied by `page`, `size`, and COUNT's `total`.
A mismatch preserves returned rows, hides stale total/pagination and replaces
empty copy with a retryable notice; COUNT and LIST are not assumed to share a
snapshot. No deployed runtime verification has been performed.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-08-API-001` | #20 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-08-API-002` | #21 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #20, #21
- Orchestration/data notes: GET #20 page/status → GET #21 nếu cần dữ liệu progress không kèm sẵn; merge theo course_id.
- BE/source status và gate: **DD BLOCKED; IMPLEMENTATION PARTIAL; RUNTIME NOT VERIFIED.** #20 route/query/view and paged Study Client caller are source-wired; current #20 returns `CourseSummaryPage`, while the catalog declares `UserProfile`. #21 route returns `UserProfile` and ST-08 does not call it for progress. AC-13 empty behavior, status filter/progress merge, legacy BIGINT vs V1-PILOT UUID alignment, loaded-state design and visual fidelity remain open.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API contract, dữ liệu và bảo mật

_Nguồn không có nội dung dưới heading này._

### Trích từ DD nguồn: API #20 — Lấy khóa đã đăng ký

| Thuộc tính | Contract đang khai báo |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/courses` |
| Authentication / authorization | `Bearer JWT`; role `Student` trong catalog. Current route is authenticated and owner-scoped; deployed auth runtime is unverified. |
| Path / query / body | Không có path param; `status?: string`, `page?: int32`; không khai báo body. Enum/default/validation chi tiết và page metadata chưa được chốt. |
| Response | `ApiEnvelope<UserProfile>` theo catalog; không đủ biểu diễn course collection theo AC-13. Không đổi sang `Page<Course>` hoặc tự thêm field. |
| HTTP/business codes | `200 DESIGN_RESOURCE_RETRIEVED`; `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `422 DESIGN_VALIDATION_ERROR`; `500 DESIGN_INTERNAL_ERROR`. Error body chưa được đối chiếu source. |
| Runtime/source status | Current route/query/view and ST-08 caller are `SOURCE_WIRED`; current response is `CourseSummaryPage`, which differs from catalog `UserProfile`. API DD is Draft — Needs Confirmation; deployed runtime is unverified. |

### Trích từ DD nguồn: API #21 — Lấy progress tổng hợp

| Thuộc tính | Contract đang khai báo |
|---|---|
| Method / endpoint | `GET /api/v1/users/me/progress` |
| Authentication / authorization | `Bearer JWT`; role `Student` trong catalog. Current route derives the user through Student auth; deployed auth runtime is unverified. |
| Path / query / body | Không có path param; catalog ghi `course_id list hoặc aggregate?:string` (cú pháp/kiểu không rõ); không khai báo body. |
| Response | `ApiEnvelope<UserProfile>` theo catalog; không xác định tiến độ/course ID, aggregation, nullability hoặc empty shape. |
| HTTP/business codes | `200 DESIGN_RESOURCE_RETRIEVED`; `401 DESIGN_AUTHENTICATION_REQUIRED`; `403 DESIGN_ACCESS_DENIED`; `500 DESIGN_INTERNAL_ERROR`. Catalog không khai báo 422 cho #21. |
| Runtime/source status | Current route returns `UserProfile`; ST-08 does not call it because it does not carry the required progress projection. API DD is Draft — Needs Confirmation; deployed runtime is unverified. |

### Trích từ DD nguồn: Data mapping và tính tiến độ

- AC-13 yêu cầu ghép khóa và progress theo `course_id`, nhưng API contract chưa khai báo course/progress DTO hoặc merge-key type.
- Legacy DDL `infra/postgres/study-server/DB.sql` có BIGSERIAL `courses`/`enrollments` và `lesson_progress(user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at)`. Đây là candidate DDL, chưa xác nhận live schema hoặc query được dùng bởi API #20/#21.
- V1-PILOT DDL `infra/postgres/02_study_db.sql` dùng course-version/enrollment model với UUID (`course_enrollments.id`, `learner_id`, `course_version_id`) và progress facts/snapshots (`lesson_progress_facts`, `progress_snapshots`). Đây là artifact thiết kế khác, không interchangeable với legacy BIGINT tables; không xác định được từ source hiện tại mô hình nào sẽ phục vụ #20/#21.
- Hai DDL artifact không xác nhận live schema, query hoặc API projection. Không suy luận `courseId` type từ `ST-09` route, API #20 query, hay legacy columns.
- DDL chưa định nghĩa ở đây cách tính aggregate theo số lesson, quiz/assignment, trạng thái hoàn tất, bài bị ẩn/đã xóa, rounding hoặc progress cho course không có lesson. Không dùng `lesson_progress.progress_percent` trực tiếp làm tổng tiến độ khóa học nếu chưa có quy tắc.
- `enrollments.status` và `courses.status` cùng tồn tại; DDL không cho biết query `status` của #20 lọc trường nào. DDL cũng không chứng minh page order, enrollment uniqueness hay missing-user behavior.
- API #37 là course progress chi tiết cho ST-09/ST-20 theo inventory; không thay #21 hoặc tự dùng làm aggregate cho ST-08 khi chưa được xác nhận.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-08_khoa-hoc-cua-toi/ST-08.md)
