# GS-05 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-05-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-05-API-002` | #10 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #10
- Orchestration/data notes: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- BE/source status và gate: **D (#10 declared; no current route/module/test)**; **BLOCK:** #08 catalog `course_id:int64` lệch route `str`/parser không giới hạn signed int64; API #10 Draft yêu cầu `Discussion.title` nhưng không có source; không có course-rating/aggregate source, literal rating-filter key/semantics hoặc public root/reply visibility approval; legacy `discussions` thiếu title/rating và V1-PILOT assessment reviews là model khác; AC-05 aggregate/eager #08→#09→#10 lệch F02 lazy tab, inventory yêu cầu #08 cache reuse; loaded review/reply/page/loading/error UI thiếu; live schema và Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: F. API contract and source status

### API #08 — public course detail prerequisite (`SOURCE_BACKED`)

| Thuộc tính | Current source |
|---|---|
| Method/path | `GET /api/v1/courses/{course_id}` registered in `apps/study-server/app/api/v1.py`. |
| Auth/input | Public; no body/query. Catalog says `course_id:int64`, but FastAPI route parameter is typed `str`; shared `parse_integer` checks syntax/Python digit ceiling, not signed-int64 or positive range. |
| Query | `courses` by ID and `status='PUBLISHED'`, LEFT JOIN public mentor projection. Read-only. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; common envelope; `data.items` contains singleton `Course` with pagination page/size/total/total_pages all 1. Course fields include id/title/description?/thumbnail_url?/price/status/mentor. |
| Errors | HTTP 404 `DESIGN_RESOURCE_NOT_FOUND` for parse failure/missing/unpublished course; HTTP 500 `DESIGN_INTERNAL_ERROR` for DB/mapping failure; current SQLAlchemy error path rolls back. Focused test source covers an ordinary ID and non-integer input, not int64 range boundaries. |
| Evidence | `apps/study-server/app/modules/guest/api_08_courses_detail/{validate.py,query.py,view.py,models.py}` and `apps/study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py`. Test source is read only; no tests run and no live schema/deployment verification. |
| UI handoff | Inventory says reuse #08, but there is no Study Web cache. Direct entry, cache miss, freshness and revalidation behavior remain open. |

### API #10 — public reviews (`DECLARED_NOT_RUNNABLE`)

| Thuộc tính | Declared/Draft evidence |
|---|---|
| Method/path | Catalog and Draft DD declare public `GET /api/v1/courses/{course_id}/reviews`. No matching route/module/test found under current `apps/study-server/app/` or `apps/study-server/tests/`. Current #97/#98 routes are `/admin/discussions/reported` and `/admin/discussions/{discussion_id}` with an `ADMIN` guard; these are moderation endpoints, not a public course-review replacement. |
| Request | Required `course_id:int64`; optional `page:int32`; literal `rating filter?:string` has unresolved physical query key/semantics. Public/no Bearer/body. |
| Response | `ApiEnvelope<Page<Discussion>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; item fields and gaps are listed in `GS05-EV-03`. No rating or aggregate field. |
| Draft data flow | Q1 checks PUBLISHED course; Q2 gets review roots; Q3 gets nested replies; Q4 counts roots. Draft suggests `parent_id IS NULL`, `status='ACTIVE'`, page size 20 and created-time/id sorting. These are not verified runtime behavior; visibility/order/pagination are marked assumptions/design-only in the DD. |
| Errors | Catalog declares 404 `DESIGN_RESOURCE_NOT_FOUND` and 500 `DESIGN_INTERNAL_ERROR`. It does not declare 401/403/422. Malformed optional query semantics remain TBD in API DD. |
| Documents | `docs/lists/list_api.md` declares endpoint/shape; `apps/study-server/docs/dd/10_courses_reviews/00_Cover.md` status is `Draft — Needs Confirmation`; request/response/mapping/error/table pages retain title/rating/schema conflicts. |
| Runtime | API #10 is `DECLARED_NOT_RUNNABLE`; no deployed behavior, live query, response, retry/cache policy or test result is claimed. |

### Database and business-rule discrepancy

- Current checked-in legacy candidate `infra/postgres/study-server/DB.sql` has `discussions(id, course_id, user_id, parent_id, content, status, created_at, updated_at)`; there is no `title`, rating value or course-rating aggregate source in that table. Its use as public reviews is an API #10 Draft mapping, not current runtime behavior. Existing #97/#98 source is Admin-only discussion moderation, not a Guest read path.
- V1-PILOT `infra/postgres/02_study_db.sql` defines `assessment_reviews` and `assessment_review_scores` keyed to assessment attempts and rubric criteria, with grading decisions/scores/feedback. These are assessment-grading records, not a course-review relation or rating aggregate for #10. Neither checked-in DDL proves the live schema; `.agents/server-study/database.md` marks live status `NOT_VERIFIED_HERE`.
- `apps/study-server/docs/dd/10_courses_reviews/02_Overview.md` itself says `Discussion.title` is required by contract but has no source; rating filter/aggregate has no schema or response field; `status='ACTIVE'` for roots/replies is an assumption needing confirmation.
- AC-05 says “Đọc review + aggregate rating.” GS-05 inventory says do not show average stars without rating contract; G-06 also records missing #10 rating/title source. Preserve this discrepancy. Do not create a score or derive one from review text/count.
- `.agents/server-study/database.md` marks checked-in DB artifacts separately from live schema; production/live PostgreSQL metadata was not inspected in this screen task.

### Trích từ DD nguồn: C.1 Expected flow — cần contract/UI wiring

1. Guest mở tab từ GS-03 với cùng `courseId` và route đề xuất `/courses/:courseId?tab=reviews`. Direct-entry không có GS-03/cache chưa có behavior được duyệt.
2. Inventory GS-05 yêu cầu reuse #08. Cache key, freshness, invalidation, cache miss, stale course và fallback #08 chưa được định nghĩa. #08 current source có thể xác nhận course PUBLISHED nếu request được thực hiện; không suy ra client sẽ tự gọi lại khi cache vắng.
3. Khi lấy reviews, F02 kỳ vọng lazy GET #10 khi chọn tab. AC-05 diagram mô tả #08 → #09 → #10 eager trước render; giữ hai yêu cầu như discrepancy, không tự chọn một luồng.
4. API #10 hiện chỉ là declared contract. Nếu được nối theo contract đã duyệt, request là public GET với `course_id` và `page` tùy chọn. `rating filter` có tên physical/semantics chưa xác nhận; không gửi query filter và không dựng rating UI từ thông tin hiện có.
5. Success 200 non-empty được kỳ vọng map review roots, authors và replies. Nhưng `title` là required trong Draft response mà thiếu data source; visibility `status='ACTIVE'` và parent/reply mapping là assumptions. Loaded card projection/design cần chốt trước implement.
6. Success 200 empty phải hiện empty state riêng, không biến thành course 404 hoặc API error. Copy hiện tại không gắn với response.
7. Course missing/unpublished 404 cần phân biệt với empty reviews. #10 Draft DD dự kiến tự gate PUBLISHED course; #08 current source cũng trả 404. No 403 contract is declared for #10.
8. Review data là read-only trên GS-05. Không thêm create/reply/report/reaction action; không có API/action source trong screen contract này.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md)
