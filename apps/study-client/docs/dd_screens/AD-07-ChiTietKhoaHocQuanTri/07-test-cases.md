# AD-07 — Test Cases

> Các mã `TC` bên dưới là planning references được tạo cho file DD; chúng không phải test suite, không được chạy và không chứng minh implementation/runtime.

## 1. Coverage matrix
| Test ID | Type | Event | Rule/API | Priority |
|---|---|---|---|---|
| `AD-07-TC-001` | Planning ref / not run | `AC-32` | See source acceptance section | P1 |

## 2. Test planning references

### AD-07-TC-001 — Acceptance planning reference (AC-32)
- **Mục tiêu:** Giữ truy vết tới yêu cầu/acceptance đã ghi; đây là test planning reference, không phải test code hoặc kết quả chạy.
- **Precondition:** Đọc nguồn [AD-07](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07.md) và gỡ blocker áp dụng trước khi implementation.
- **Mock/test data:** Nguồn không cung cấp fixture dùng để chạy test ở package này; không đưa dữ liệu thật.
- **Steps:**
  1. Đối chiếu acceptance và event tương ứng trong DD nguồn.
  2. Khi runtime/test implementation tồn tại, viết test riêng theo contract đã xác nhận.
- **Expected UI/state:** Theo acceptance/state trong nguồn; chưa được xác minh trên runtime.
- **Expected API/data:** Theo [API Integration](04-api-integration.md); không phát sinh request trong lần tạo tài liệu.
- **Failure / edge assertion:** Không đánh dấu pass cho `UNWIRED`, `IMPLEMENTATION BLOCKED` hoặc `RUNTIME NOT VERIFIED`.
- **References:** `AC-32`, [Events](02-events.md), [Business Rules](05-business-rules.md), [source DD](../../screen_stitch/05_admin/AD-07_chi-tiet-khoa-hoc-quan-tri/AD-07.md).

## 3. Source acceptance / test plan (not run)

### Trích từ DD nguồn: F. Tiêu chí nghiệm thu

- [x] Expected behavior and current behavior are separated, with source/prototype/runtime evidence labeled.
- [x] AC-32 ↔ AD-06/AD-08/AD-09/AD-12 relations and numeric ID handoff are documented; #82 course filter capability and unresolved route/cardinality are explicit.
- [x] API #74 is checked against catalog, route, view, SQL, shared Course model/mapper and existing tests; no unsupported API field is assumed.
- [x] All 56 visible prototype regions map to a unique marker and C row.
- [x] Load, mapping, back/edit/status-delete/lessons navigation, unsupported controls, access/errors, nullable fields and session-expiry gap are described.
- [x] API error/status mapping and read-only effects are documented; retry/cache/permission/counter/cardinality policies remain explicit open questions.
- [x] No course-code/counter/curriculum/quality rule or mutation behavior is invented.
- [ ] Owner resolves blockers: course-management permission, counters, singleton cardinality, live schema, CourseStatus/null/mentor policy, AD-08/09 handoffs, and AD-12 query-route/#82 cardinality.
- [ ] Study Web route/API integration and runtime behavior are implemented and verified separately.

**Decision:** `DD BLOCKED` until the open data, permission and navigation contracts are resolved. **Implementation:** `IMPLEMENTATION BLOCKED`. **Runtime:** `NOT VERIFIED` because Study Web is unwired. API #74 reverse source index can be `R`; API DD remains `Draft — Needs Confirmation`.

#### Kế hoạch kiểm chứng từ source PLAN

### Trích từ DD nguồn: 2. Bằng chứng rà soát

| Nhóm | Nguồn | Kết luận cho AD-07 |
|---|---|---|
| Inventory/dependency | `list_screen.md` rows 64–70; `dd_screens/PLAN.md` rows AD-06–AD-12 | AD-06 opens AD-07 with numeric `Course.id`; proposed `/admin/courses/:courseId`; related AD-08/09/12. Inventory says counters “if API returns”; it currently does not. |
| AC-32 | `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` | Admin precondition: course-management permission. Sequence GET #73 → GET #74 reading course/owner/counters → choose PUT #75, PATCH #76, or DELETE #77 by operation/policy → reload management. Counter field/definition is absent from response contract. |
| API catalog #74 | `docs/lists/list_api.md` | `GET /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, required `course_id:int64`; `ApiEnvelope<Page<Course>>`; 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500. No request body/query or 422 entry. |
| API #74 source | `apps/study-server/app/api/v1.py`; `modules/admin/api_74_admin_course_detail/{view,query,validate,models}.py` | Route is registered. Shared ADMIN guard precedes path parse and DB. Parser accepts signed-int64, including negative, and rejects malformed/out-of-range as 404. Bound query reads course+mentor without status filter. Response is one `Course` in a singleton `Page` (pagination 1/1/1/1); read-only/no commit. Query/projection/map errors become safe 500 with rollback. |
| Course response mapping | `guest/_shared/course_catalog/{models,helpers}.py` | `id`, `title`, nullable `description`, nullable `thumbnail_url`, exact decimal-string `price`, `status`, `mentor{id,full_name,avatar_url|null}`. No course code, category, counters, curriculum/lessons, enrollments, or conversion fields. |
| API #74 authorization gap | AC-32 diagram vs `validate.py` and core auth guard | AC requires course-management permission. Local implementation verifies shared JWT role `ADMIN` only; it does not independently check the fine-grained permission. Mapping is unresolved. |
| Database | `infra/postgres/study-server/DB.sql`; versioned pilot DDL references in API #74 DD | Legacy candidate uses BIGINT `courses.id`, `mentor_id`, `name`, `price`, `status`; versioned pilot artifacts differ. Live schema/deployment is unknown. |
| API test evidence | `apps/study-server/tests/modules/admin/api_74_admin_course_detail/test_admin_course_detail.py`; API #74 `VERIFICATION_REPORT.md` | Existing focused unit source covers singleton mapping, auth-before-parse/query, signed/malformed paths, 404, safe 500 and OpenAPI. Fake DB doubles are not live DB proof. Historical HTTP run is temporary-schema evidence. No tests run in this screen session. |
| AD-12/API #82 handoff | `docs/lists/list_api.md`; `app/api/v1.py`; `modules/admin/api_82_admin_lessons_list/{validate,query,view}.py`; API #82 `OPEN_QUESTIONS.md` | Catalog/source accept exact optional `course:int64` filtering; a numeric Course ID can be carried as `?course=<id>`. This is a route-handoff candidate, not inventory-approved navigation. API #82 DD is Draft; catalog `ApiEnvelope<Lesson>` conflicts with local `ApiEnvelope<Lesson[]>`. |
| API DD | `apps/study-server/docs/dd/74_admin_course_detail/` | `Draft — Needs Confirmation`; open questions include permission, counters, live schema, mentor integrity/nulls, status semantics and visibility after #77. |
| Prototype/current UI | `screen.png`, `code.html`, `.agents/web-work/study/*` | Static blank detail mockup; hard-coded metrics/empty curriculum/quality claims. Anchors use `#`; outgoing AD-08/09/12 buttons disabled; no request or navigation handlers. Study Web app source/package/router absent (`UNWIRED`). |

### Trích từ DD nguồn: 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type docs worklogs and prescribed context/source pages.
2. [x] Review inventory, prototype/image, AC-32, API #74 catalog/DD/source/tests, candidate DDL and Study Web boundary; record expected/current and discrepancies.
3. [x] Write this plan before marker map, annotation and DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated image; preserve source hashes.
5. [x] Author A–F DD with one C row per marker, source-traced events/API/errors/states/navigation and visible blockers.
6. [x] Update AD-07 inventory/reverse API source index and global tracker/checkpoint.
7. [x] Verify hashes, dimensions, marker sequence/coordinates/1:1 C rows, local links, 83 screen IDs/folders, core artifact count, whitespace and image appearance. Do not run app tests/runtime.
8. [x] Update worklog with final verification; do not process another Screen ID.

- Runtime status: `RUNTIME NOT VERIFIED` (the generated DD does not claim otherwise).
- Không chạy app test trong task chuyển đổi tài liệu.
