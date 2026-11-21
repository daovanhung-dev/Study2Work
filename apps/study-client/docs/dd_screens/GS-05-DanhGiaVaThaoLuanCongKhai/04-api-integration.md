# GS-05 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

> **Current implementation update (T021, 2026-11-17):** API #10 route/module/test and GS05 Web caller now exist in source. The client sends only `page`; its loaded panel renders source-backed author/content/replies and pagination. API #10 DD remains `Draft — Needs Confirmation`; T021's browser render used a temporary in-memory stub, not live API/DB/deployment.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `GS-05-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `GS-05-API-002` | #10 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #10
- Orchestration/data notes: Tái dùng #8 → GET #10 phân trang; 404 course riêng với empty reviews.
- BE/source status và gate: **#10 SOURCE_BACKED locally; Study Web caller WIRED; API DD Draft**; **BLOCK:** #08 catalog `course_id:int64` vs route `str`; API #10 Draft requires `Discussion.title` without source; no course-rating/aggregate source, rating query key/semantics, or approved public root/reply visibility; legacy/V1-PILOT schemas are not live-schema evidence; AC-05 aggregate/eager differs from F02 lazy; no client cache; loaded projection has no approved visual design; live DB/deployment unverified.
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

### API #10 — public reviews (`SOURCE_BACKED`; DD `Draft — Needs Confirmation`)

| Thuộc tính | Declared/Draft evidence |
|---|---|
| Method/path | Public `GET /api/v1/courses/{course_id}/reviews` is registered in `apps/study-server/app/api/v1.py`; implementation is in `app/modules/guest/api_10_courses_reviews/`, with focused tests under `apps/study-server/tests/modules/guest/api_10_courses_reviews/`. #97/#98 remain separate ADMIN moderation APIs. |
| Request | Current route takes the path ID as text and query model includes optional `page` and `rating`; the GS05 client sends only `page` (default 1) and no Bearer/body. The rating key/semantics remain unresolved and source does not apply a rating filter. |
| Response | Current source returns `ApiEnvelope<Page>` with root content/author, nested reply content/author, `title: null`, root `created_at`, status and page metadata. No rating/aggregate. This differs from the Draft-required title and response details. |
| Current data flow | Source checks course `PUBLISHED`; reads root discussions with `parent_id IS NULL` and `status='ACTIVE'`, sorted by `created_at DESC, id DESC`, page size 20; reads ACTIVE replies for current roots without an explicit reply order; counts matching roots. These are current code behaviors, not approval of the public-visibility/business rules or proof of live schema. |
| Errors | Source returns 404 `DESIGN_RESOURCE_NOT_FOUND` for no published course and 500 `DESIGN_INTERNAL_ERROR` for current query/mapping error paths. DD does not declare 401/403/422; malformed optional query semantics remain unresolved. |
| Documents | `docs/lists/list_api.md` declares endpoint/shape; `apps/study-server/docs/dd/10_courses_reviews/00_Cover.md` status is `Draft — Needs Confirmation`; request/response/mapping/error/table pages retain title/rating/schema conflicts. |
| Verification/runtime | Focused source-backed API suite: 22 passed using fake/overridden DB sessions. Study Web GS03+GS05 focused specs: 12/12; full Study Web suite: 153/153. Desktop/mobile headless Chrome rendered using a temporary in-memory local API stub. No live API request, DB schema, deployment, retry or cache behavior was verified. |

### Database and business-rule discrepancy

- Current Study Server #10 source reads the `discussions` relation for public GET results. The checked-in legacy candidate `infra/postgres/study-server/DB.sql` has `discussions(id, course_id, user_id, parent_id, content, status, created_at, updated_at)` and no `title`, rating value or course-rating aggregate field; current query/source does not resolve whether the deployed schema/publication policy is approved. Existing #97/#98 are separate Admin moderation paths.
- V1-PILOT `infra/postgres/02_study_db.sql` defines `assessment_reviews` and `assessment_review_scores` keyed to assessment attempts and rubric criteria, with grading decisions/scores/feedback. These are assessment-grading records, not a course-review relation or rating aggregate for #10. Neither checked-in DDL proves the live schema; `.agents/server-study/database.md` marks live status `NOT_VERIFIED_HERE`.
- `apps/study-server/docs/dd/10_courses_reviews/02_Overview.md` itself says `Discussion.title` is required by contract but has no source; rating filter/aggregate has no schema or response field; `status='ACTIVE'` for roots/replies is an assumption needing confirmation.
- AC-05 says “Đọc review + aggregate rating.” GS-05 inventory says do not show average stars without rating contract; G-06 also records missing #10 rating/title source. Preserve this discrepancy. Do not create a score or derive one from review text/count.
- `.agents/server-study/database.md` marks checked-in DB artifacts separately from live schema; production/live PostgreSQL metadata was not inspected in this screen task.

### Trích từ DD nguồn: C.1 Expected flow — cần contract/UI wiring

1. Current GS03 owns `/courses/:courseId?tab=reviews`; direct entry requests #08, then mounts GS05/#10 after the published-course response. The #08 result is not stored in a shared client cache; cache/freshness policy remains undefined.
2. Inventory GS-05 yêu cầu reuse #08. Cache key, freshness, invalidation, cache miss, stale course và fallback #08 chưa được định nghĩa. #08 current source có thể xác nhận course PUBLISHED nếu request được thực hiện; không suy ra client sẽ tự gọi lại khi cache vắng.
3. Current FE follows F02 lazy tab loading; AC-05 diagram still describes #08 → #09 → #10 eager before rendering/aggregate rating. The implementation records this as a discrepancy, not an approved resolution.
4. Current GS05 sends public GET with route `course_id` and `page` only; it sends no rating filter and renders no rating UI. Rating key/semantics remain unresolved.
5. Success 200 non-empty maps root/reply author name and content plus `page/total_pages`; title, IDs, status, timestamps, rating and aggregate are not rendered. This bounded projection and loaded card design are implementation choices without DD visual approval; visibility rules remain Draft.
6. Success 200 empty is response-bound and shows a separate empty state; tests cover it.
7. Course missing/unpublished 404 cần phân biệt với empty reviews. #10 Draft DD dự kiến tự gate PUBLISHED course; #08 current source cũng trả 404. No 403 contract is declared for #10.
8. Review data là read-only trên GS-05. Không thêm create/reply/report/reaction action; không có API/action source trong screen contract này.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md)
