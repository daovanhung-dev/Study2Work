# AD-08 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-08-API-001` | #74 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-08-API-002` | #75 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #74, #75
- Orchestration/data notes: GET #74 → PUT #75 → revalidate #74; không có API create admin course ở V1. #75 locally returns an updated Course projection; whether the UI also re-fetches #74 is open.
- BE/source status và gate: **R**; #75 route/module/test source exists, API DD remains Draft. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/AC omit PUT body; local four-field full-replacement body and rules are DERIVED; thumbnail upload contract absent; mentor edit mockup conflicts with #75; AC-32 permission vs `ADMIN`, legacy/live schema, response/revalidation and Study Web UNWIRED remain open; Back/Cancel currently point to AD-06; **RUNTIME NOT VERIFIED**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: API matrix — #74 / #75

| API | Method / endpoint | Auth | Request | Response / mapping | Errors and source status |
|---|---|---|---|---|---|
| #74 | `GET /api/v1/admin/courses/{course_id}` | Bearer JWT; catalog says Admin. AC-32 fine-grained permission mapping remains open. | Path `course_id:int64`; no body/query. | Catalog `ApiEnvelope<Page<Course>>`; local source reads Course + mentor and returns singleton page. Candidate load/revalidation for AD-08. | Catalog: 401/403/404/500. Local source exists; API DD Draft; live schema/runtime not verified. |
| #75 | `PUT /api/v1/admin/courses/{course_id}` | Bearer JWT; catalog says Admin; local guard checks shared role `ADMIN`. | Path `course_id:int64`; catalog/AC body absent. Local strict candidate body: required title, description, thumbnail_url, price. Content-Type JSON is needed for current body but not specified by catalog. | Catalog `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_UPDATED`. Local response uses `Course updated.` and one Course with singleton pagination via #74 projection. | Catalog: 401/403/404/422/500. Local errors as EV-04; route/module/test source exists. API DD `Draft — Needs Confirmation`; implementation is API-only, Study Web unwired. |

**#75 request candidate — DERIVED, owner approval required**

| Key | Local type / presence | Local current validation and mapping | Contract status |
|---|---|---|---|
| `title` | strict string; required | Max 200 characters from current validator/legacy candidate; no trim or nonblank check; SQL maps to `courses.name`. | Catalog/AC omit body; `DERIVED`. |
| `description` | strict string or null; key required | Null can clear candidate column; no max in #75 validator. | Catalog/AC omit body; `DERIVED`. |
| `thumbnail_url` | strict string or null; key required | No URI scheme/host/length check; maps as URL string; no file upload. | Catalog/AC omit body; upload contract not found. |
| `price` | strict decimal string; required | Regex rejects exponent, scale ≤2, absolute integer digits <10¹⁰; negatives accepted; parsed to Decimal then bound SQL. Legacy `NUMERIC(12,2)` is only a candidate. | Catalog/AC omit body; `DERIVED`. |

Do not extend the candidate body with `mentor_id`, course code, `status`, category, chapter/enrollment metrics, `row_version` or an uploaded file without an approved API change. The local source does not document a client retry/cache policy, optimistic concurrency contract or upload endpoint.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global screen plan](../../screen_stitch/dd_screens/PLAN.md) · [AC-32 admin flow](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API catalog](../../../../../docs/lists/list_api.md) · [API #75 route](../../../../study-server/app/api/v1.py) · [request model](../../../../study-server/app/modules/admin/api_75_admin_course_update/models.py) · [validator](../../../../study-server/app/modules/admin/api_75_admin_course_update/validate.py) · [view](../../../../study-server/app/modules/admin/api_75_admin_course_update/view.py) · [SQL](../../../../study-server/app/modules/admin/api_75_admin_course_update/query.py)
- [API #75 open questions](../../../../study-server/docs/dd/75_admin_course_update/OPEN_QUESTIONS.md) · [API #75 verification report](../../../../study-server/docs/dd/75_admin_course_update/VERIFICATION_REPORT.md) · [API #75 tests](../../../../study-server/tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py)
- [API #74 detail source](../../../../study-server/app/modules/admin/api_74_admin_course_detail/query.py) · [Course response model](../../../../study-server/app/modules/guest/_shared/course_catalog/models.py) · [legacy schema candidate](../../../../../infra/postgres/study-server/DB.sql) · [V1-PILOT Course schema](../../../../../infra/postgres/02_study_db.sql)
- [Study Web design context](../../../../../.agents/web-study/design.md) · [Study Web scope index](../../../../../.agents/web-work/study/INDEX.md)

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-08_chinh-sua-khoa-hoc/AD-08.md)
