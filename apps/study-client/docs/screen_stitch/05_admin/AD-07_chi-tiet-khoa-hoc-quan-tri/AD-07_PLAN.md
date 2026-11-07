# AD-07 — Kế hoạch Detailed Design

> **Screen ID:** AD-07 · **Tên:** Chi tiết khóa học quản trị · **Đợt/ưu tiên:** W4 / P1<br>
> **Route đề xuất:** `/admin/courses/:courseId` · **AC:** AC-32 · **API chính:** #74<br>
> **Trạng thái inventory trước phiên:** `D`; API #74 has local route/module/tests. API DD is `Draft — Needs Confirmation`; Study Web is `UNWIRED`.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện riêng AD-07 trong phiên này: source trace, plan trước marker/DD, marker map, annotated image, A–F DD, inventory/reverse API index, global tracker và worklog. Không bắt đầu AD-08.
- Giữ nguyên `screen.png` và `code.html`; chỉ thêm `<ID>_PLAN.md`, `<ID>.md`, `<ID>_markers.json`, marker overlay SVG và `screen_annotated.png`.
- Dùng numeric `Course.id` từ AD-06 làm `courseId` candidate route/path value; không suy ra ID từ nhãn “Mã khóa học”.
- Phân biệt AC/catalog, local API source, prototype, isolated API tests/report và runtime/deployment. Không nâng API DD draft hoặc legacy DDL thành quyết định đã duyệt/live.
- Không bịa `course_code`, counters, curriculum, lesson count, category, conversion, enrollment, quality/compliance rules, CourseStatus enum, retry/cache policy, route/query handoff, or permission mapping.
- API #74 là read-only. AD-08/#75 và AD-09/#76/#77 là downstream AC-32 branches. AD-12/#82 is inventory-listed; API #82 catalog/local source supports an exact `course?:int64` filter, so `/admin/lessons?course=<Course.id>` is a supported handoff candidate. Inventory does not state this route query and API #82 catalog cardinality conflicts with local list response; confirm before wiring.
- Manifest has no canonical skill wired for `web-ui-only-dd`; the registered `createDD-markdown` skill excludes this boundary. No skill is loaded.
- No application tests or runtime will be run; static artifact verification is required.

## 2. Bằng chứng rà soát

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

## 3. Expected behavior và current behavior

### Expected behavior

1. Admin with the approved course-management permission reaches AD-07 from AD-06 with a numeric `Course.id`; proposed route is `/admin/courses/:courseId`.
2. The screen requests API #74 using `Authorization: Bearer <JWT>` and `course_id:int64`; it renders only fields present in the confirmed response.
3. On success, the intended projection is `Page<Course>` per catalog. Local source currently emits exactly one Course with singleton pagination; singleton cardinality remains a source implementation detail to confirm against the API DD/product contract.
4. AC-32 places update/status/delete branches after the detail read. AD-08/#75 and AD-09/#76/#77 remain separate screens/actions. API #82 supports `course?:int64`, making `/admin/lessons?course=<Course.id>` a technically supported AD-12 handoff candidate; inventory does not explicitly approve this query route and #82 cardinality remains Draft.
5. Counters, course code, curriculum, lesson list, conversions/enrollment, compliance/quality claims and any edit/status/delete action are not enabled by #74 response alone.

### Current behavior

- `code.html` is a static visual with blank data, “waiting for courseId”, hard-coded `0 khóa`, empty module text, quality statements, `href="#"` links, and disabled outgoing buttons. It has no API/navigation behavior.
- API #74 locally performs role guard → signed-int64 path parse → bound `courses LEFT JOIN users` lookup by ID → Course map → singleton Page response. It does not return the mockup's course code, counters, lessons, enrollment/conversion or quality fields.
- Malformed/out-of-int64 and missing IDs return 404. Query or incomplete/invalid required mapping returns safe 500 with rollback. Local auth failures return 401/403 before parsing/query. API #74 has no 422 catalog response. There is no client session recovery policy established by these sources.
- Study Web has no editable route/client in the current checkout, so runtime is `NOT VERIFIED` / `UNWIRED`.

### DISCREPANCIES

1. AC-32 says read counters; #74 catalog/model/query has no counter. Count names, source and meaning are open.
2. AC-32 precondition says course-management permission; local API checks role `ADMIN` only. Dedicated permission mapping/policy is open.
3. Prototype course code, metrics, curriculum/lessons, and quality/compliance claims are static and have no source in #74.
4. Inventory route uses `:courseId`, API path uses `{course_id:int64}`; ID conversion is a naming handoff only. Positive-only route validation is not established; local parser accepts negative signed-int64 and then normally gets 404.
5. AC-32 sequence links detail to #75/#76/#77 branches; exact UI route/authorization/policy and return state are not confirmed. API #82 accepts `course?:int64`, but using it in the AD-12 route and resolving its catalog `Lesson` vs local `Lesson[]` response remain open.
6. API DD is Draft and live DB/deployment is not verified; Study Web is UNWIRED.

## 4. Marker plan

Plan **56 ordered markers**, from the Admin shell through the content sections and footer. Each marker maps one-to-one to one `C` table row. Marker rows may group a heading with its subtitle only when they form one visual section; separate values or actionable controls remain separate markers.

1–11. Admin brand/nav group, five individual nav entries/notification, system status, admin identity, global breadcrumb, RBAC assurance.<br>
12–20. Local breadcrumb group, list link, current detail crumb, back link, hero API badge, screen ID, title, subtitle, load/sync status.<br>
21–38. Overview header, schema badge, empty-state icon/copy, AD-06 CTA, five metadata fields including unsupported course code, metrics icon/title/count, curriculum heading/empty badge/placeholder/copy/API-required badge.<br>
39–53. Management header and disabled AD-08/AD-09/AD-12 controls, lock note, standards header, three static standards cards with their claim badges, manual/PDF row.<br>
54–56. Footer copyright/system caption and privacy/RBAC/support links.

Source image is 1411×1600. Keep it untouched; render the annotated output at 2822×3200. Put compact numbered circles in nearby icon/empty space so labels and values remain legible.

## 5. Event and state coverage plan

| Event | Trigger | Planned treatment |
|---|---|---|
| EV-01 Enter/load detail | Direct route or selection from AD-06 | Target request #74. Describe input `courseId`, guard/path/DB order as current API source; map 200, 401, 403, 404, 500; prototype has no request. Query, retry, timeout, cache and session-expiry navigation policies remain unspecified. |
| EV-02 Return to AD-06 | Back breadcrumb/button | Current link is `#`; target returns to list. Preserve/restore search/page/filter state only if a cross-screen router contract defines it. No API call is implied by the link. |
| EV-03 Open AD-08 | Edit action after course is loaded | Current button disabled. Target handoff is selected numeric ID to proposed `/admin/courses/:courseId/edit`; AC-32 GET detail precedes PUT #75; body/save rules belong to AD-08 and remain blocked. |
| EV-04 Open AD-09 | Status/delete action after course is loaded | Current button disabled. Target handoff of numeric ID to proposed `/admin/courses/:courseId/actions`; AC-32 branch selects #76 or #77 per approved policy. Do not derive transition/delete confirmation semantics here. |
| EV-05 Open AD-12 | Related lesson-list action | Current button disabled. API #82 catalog/local source support exact `course?:int64`; `/admin/lessons?course=<Course.id>` is a supported handoff candidate. Inventory route/query choice and #82 response cardinality (`Lesson` catalog vs local list) need confirmation. |
| EV-06 Render Course fields | #74 returns valid data | Map only `id`, title, description, thumbnail, price, status, mentor. Missing required local projection currently becomes 500; optional description/thumbnail/avatar may be null. Do not bind course-code field to ID. |
| EV-07 Render absent metrics/curriculum/standards | #74 success | #74 has no source values. Treat mockup's 0, empty curriculum and quality statements as static prototype-only; do not compute counters or assert compliance. |
| EV-08 Access/resource/service errors | #74 returns 401/403/404/500 or network failure | Distinguish auth, forbidden, not found and service/network states. API response mapping is source-backed; client copy/retry/session redirect is not. Do not show errors as an empty course. |
| EV-09 Static shell/quality/PDF controls | Click header/footer/manual/PDF anchors | Current href is `#`, no handler/destination/download. Record as nonfunctional presentation until route/resource is specified; no implied API call. |

Candidate states: initial, loading, ready, not-found (404), unauthorized (401/session invalid), forbidden (403), service-error (500), network-error (client-side future), and `UNWIRED` static prototype. Empty list is not a valid #74 success state under current local singleton model; do not invent empty-course behavior. No explicit retry/cache policy is specified.

## 6. Open decisions / blockers

1. Approve whether JWT role `ADMIN` satisfies AC-32 course-management permission or define a separate permission check.
2. Define AC-32 counters, fields, source and calculation before showing metrics.
3. Confirm singleton `Page<Course>` detail cardinality and envelope semantics in API DD.
4. Confirm live schema/deployment and mentor integrity/null policy; local source requires mentor id/name and price.
5. Confirm CourseStatus values/casing and whether `DELETED` remains readable after #77.
6. Define what AD-08/AD-09 actions and routes permit, and how return-to-list state works.
7. Confirm AD-07 should pass Course.id as `course` in the AD-12 route, and resolve API #82's catalog `ApiEnvelope<Lesson>` vs local `ApiEnvelope<Lesson[]>` response before wiring the list.
8. Remove or contract source the mockup course code, curriculum/lesson list, metrics, compliance badges and PDF/manual destinations.
9. Implement/wire Study Web route, auth/client API layer and shared error/session handling, then verify runtime separately.

## 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type docs worklogs and prescribed context/source pages.
2. [x] Review inventory, prototype/image, AC-32, API #74 catalog/DD/source/tests, candidate DDL and Study Web boundary; record expected/current and discrepancies.
3. [x] Write this plan before marker map, annotation and DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated image; preserve source hashes.
5. [x] Author A–F DD with one C row per marker, source-traced events/API/errors/states/navigation and visible blockers.
6. [x] Update AD-07 inventory/reverse API source index and global tracker/checkpoint.
7. [x] Verify hashes, dimensions, marker sequence/coordinates/1:1 C rows, local links, 83 screen IDs/folders, core artifact count, whitespace and image appearance. Do not run app tests/runtime.
8. [x] Update worklog with final verification; do not process another Screen ID.

## 8. Completion decision

Expected outcome: API #74 reverse source index becomes `R` because local route/module/tests exist; its API DD remains Draft. AD-07 screen DD remains `DD BLOCKED` while counters, permission, schema/cardinality, mockup-only data and navigation decisions are open. Implementation is `IMPLEMENTATION BLOCKED` because Study Web is unwired and the action/permission/data contracts are unresolved. Study Web runtime is `NOT VERIFIED`.
