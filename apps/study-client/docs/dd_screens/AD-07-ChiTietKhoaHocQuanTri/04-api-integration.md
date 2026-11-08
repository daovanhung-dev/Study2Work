# AD-07 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-07-API-001` | #74 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #74
- Orchestration/data notes: GET #74 with numeric `Course.id`; do not use public GET #8. AC-32 then branches to #75/#76/#77. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a handoff candidate pending route approval and #82 response-contract resolution.
- BE/source status và gate: **R** source/API #74 route/module/test; API DD `Draft — Needs Confirmation`; **DD BLOCKED; IMPLEMENTATION BLOCKED:** counter definition, AC-32 permission mapping, singleton Page/live schema, prototype-only course code/metrics/curriculum/quality claims, AD-12 query-route approval/#82 `Lesson` vs `Lesson[]` response, and Study Web `UNWIRED` remain open; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API request/response matrix

| Thuộc tính | API #74 |
|---|---|
| Method / endpoint | `GET /api/v1/admin/courses/{course_id}` |
| Authentication / authorization | Header `Authorization: Bearer <JWT>`; catalog says role Admin. Local route uses shared JWT role `ADMIN`. AC-32 fine-grained course-management permission is not separately enforced in local #74; mapping is open. |
| Path params | `course_id:int64!`; no query params, request body, or other API-specific header is listed. Client route name `courseId` is only a route variable. |
| Success schema | Catalog: `ApiEnvelope<Page<Course>>`. Local envelope fields: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`. Local `data.items` contains one Course and pagination page/size/total/total_pages are all `1`. Singleton cardinality remains `DERIVED` pending API DD confirmation. |
| Course mapping | `id:int`; `title:string`; `description:string|null`; `thumbnail_url:string|null`; `price:string` exact decimal; `status:string`; `mentor:{id:int,full_name:string,avatar_url:string|null}`. No `course_code`, counters, category in local #74 model/query, curriculum, lesson count, enrollment or conversion field. |
| Query/effects | Read-only bound SQL: `courses` LEFT JOIN `users`, predicate `c.id = :course_id`, `LIMIT 1`; no status filter. No insert/update/delete, commit, audit or cache mutation. Legacy DDL is candidate only; live schema not verified. |
| Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, “Course retrieved.” according to local source/catalog. |
| Errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 500 `DESIGN_INTERNAL_ERROR`. API catalog does not declare 422. Local malformed/out-of-range path → 404 before query; missing row → 404; query/mapping failure → safe 500 and rollback. |
| Ordering | One #74 call per detail load in target; no dependent request is defined. AC-32 places #74 after #73 and before its #75/#76/#77 branches. |
| Retry / timeout / cache | Not specified by API catalog/DD or UI source. Do not select a client policy in this DD. GET has no mutation/idempotency body; any cache freshness remains open. |
| Test/runtime evidence | Local route/module/test source exists. Existing tests use fake session/query doubles. A historical verification report used a temporary schema; neither proves current live DB/deployment. No tests or runtime were run in this session. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07.md)
