---
task_id: "2026-11-22-enable-admin-course-creation"
date: "2026-11-22"
primary_task_type: "fix"
secondary_task_types: ["coding", "test", "docs"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web AD-06 -> Study Server API #104 POST /admin/courses; mentor options use Admin API #68"]
status: "COMPLETE"
---

# Worklog: Enable Admin course creation

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Supplied router context | Follow task classification, read-set, and source boundaries; do not reopen. | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Read-set, target, and worklog rules | Global task policy. | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Canonical load flow and Study scope graph | Resolve Web ↔ Study Server dependency. | `READ_FROM_CONTEXT` |
| `.agents/context-manifest.json` | web-work/server-study, code-review, fix and screen workflow registry entries | Confirm current routing. | `READ_FROM_CONTEXT` |
| `.agents/project/agent-control.md` | Target/read-set/worklog rules | Track leaf targets and preserve prior work. | `READ_FROM_CONTEXT` |
| `.agents/target.md` | Full file | Active target tracker. | `READ_FROM_CONTEXT` |
| `.agents/worklog/README.md` | Preflight and required order | Worklog contract. | `READ_FROM_CONTEXT` |
| `.agents/worklog/TEMPLATE.md` | Full template | Required sections. | `READ_FROM_CONTEXT` |
| `scripts/select-worklogs.mjs` | Exact-type selector | Select prior fix worklogs. | `CHECKED_BY_TOOL` |
| `scripts/validate-agent-context.mjs` | Run validator and compare findings with recorded baseline | Required after context changes. | `RUN_EXIT_1_BASELINE_IDENTICAL` |
| `.agents/worklog/2026-11-22/enable-admin-course-creation.md` | Selector self-match; metadata only | Do not treat the active worklog as prior evidence. | `SKIPPED` |
| `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md` | Audit result, source trace, runtime limits | Carry forward the immediately prior AD-06 findings. | `READ` |
| `.agents/worklog/2026-11-22/fix-study-admin-overview-summary.md` | Related API/runtime boundaries and current dirty-state handoff | Preserve previous Admin changes and avoid conflating AD-01 with AD-06. | `READ` |
| `.agents/project/INDEX.md` | Study API/client boundary | Cross-scope contract context. | `READ` |
| `.agents/project/workflows.md` | Fix/coding/test/worklog workflows | Required implementation sequence. | `READ` |
| `.agents/project/contracts.md` | Study API contract status and change rules | Register new API contract safely. | `READ` |
| `.agents/web-work/AGENTS.md` | Current Web rules | Preserve Angular/React boundary and source rules. | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web screen rules | Apply AD-06 screen constraints. | `READ` |
| `.agents/web-work/study/INDEX.md` | AD-06, AD-07/08, API #68/#73/#75 and verification facts | Current page/mentor source map. | `READ_EDITED` |
| `.agents/web-work/study/workflows/screen-implementation.md` | Preflight, DD, event/API, demo and verification requirements | Implement within the screen workflow. | `PLANNED` |
| `.agents/web-study/design.md` | Admin dialog/form/accessibility guidance | Match existing Study Web design. | `PLANNED` |
| `.agents/web-study/frontend-rules.md` | Study Web layers, forms, API and test rules | Place changes in canonical folders. | `PLANNED` |
| `.agents/server-study/AGENTS.md` | Server conventions and no-invention rules | API #104 implementation boundary. | `READ_EDITED` |
| `.agents/server-study/INDEX.md` | API #68/#73/#75/#88 pages and route links | Locate current module/test patterns. | `PLANNED` |
| `.agents/server-study/apis/declared-routes.md` | Admin API route inventory | Register API #104 without collision. | `READ_EDITED` |
| `.agents/server-study/modules/README.md` | Admin module layer conventions | Implement model/validate/query/view correctly. | `READ_EDITED` |
| `.agents/server-study/core/runtime.md` | Router, envelopes, exceptions and trace ID | Match API response behavior. | `PLANNED` |
| `.agents/server-study/core/database-security.md` | Authorization and DB transaction helpers | Enforce Admin/mentor validation and transaction. | `PLANNED` |
| `.agents/server-study/tests.md` | Focused test conventions | Add API regression tests. | `READ_EDITED` |
| `.agents/server-study/workflows/README.md` | Fix workflow and verification commands | Run focused server checks. | `PLANNED` |
| `apps/study-client/docs/dd_screens/screen-index.md` | AD-06 package pointer | Locate the eight DD sections and screenshot references. | `PLANNED` |
| `apps/study-client/docs/dd_screens/` | Bounded filename inventory only | Locate AD-06 DD and clean/numbered reference images. | `PLANNED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/00-overview.md` | Full section | Scope/status and design constraints. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/01-ui-elements.md` | Full section | Current create control and form elements. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/02-events.md` | Full section | Button/dialog and submit events. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/03-data-flow.md` | Full section | API-backed data flow. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/04-api-integration.md` | Full section | Current API contract gaps and planned #104. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/05-business-rules.md` | Full section | Create rules and unresolved constraints. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/06-navigation.md` | Full section | Dialog success route behavior. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/07-test-cases.md` | Full section | Regression acceptance scenarios. | `READ_EDITED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/images/README.md` | Full file | Interpret reference images/status. | `PLANNED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/images/screen-clean.png` | Visual image | Compare clean reference. | `PLANNED` |
| `apps/study-client/docs/dd_screens/AD-06-DanhSachKhoaHocQuanTri/images/screen-numbered.png` | Visual image | Map annotated elements. | `PLANNED` |
| `apps/study-client/docs/screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/` | Bounded filename inventory; then the AD-06 HTML/README/image files | Inspect approved page design and form affordance. | `PLANNED` |
| `apps/study-client/docs/screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06.md` | Screen source notes | Confirm Stitch intent and screen scope. | `PLANNED` |
| `apps/study-client/docs/screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/AD-06_PLAN.md` | Relevant plan sections | Confirm source-to-screen notes. | `PLANNED` |
| `apps/study-client/docs/screen_stitch/05_admin/AD-06_danh-sach-khoa-hoc-quan-tri/code.html` | Full HTML structure | Reuse existing visual structure for dialog. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD06/` | Page/data-access/model/UI source and test files | Implement dialog and API #104 caller. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD06/pages/ad06-page.ts` | Full component state and handlers | Add create state and submit behavior. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/pages/ad06-page.html` | Header/actions/table states | Open dialog from Add control and render dialog. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/pages/ad06-page.css` | Dialog/form-related selectors | Match existing AD-06 styling. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/pages/ad06-page.spec.ts` | Full test suite | Add create-dialog/request regression cases. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/data-access/ad06-api.service.ts` | Current API methods | Add API #104 caller. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/data-access/ad06-api-boundary.ts` | Boundary declaration | Mark create capability source-backed. | `READ` |
| `apps/study-client/src/app/features/admin/AD06/ui/ad06-screen.ui.ts` | Screen definition/actions | Keep UI definition aligned if it owns Add control metadata. | `READ` |
| `apps/study-client/src/app/features/admin/AD02/` | Bounded filename inventory and API #68 caller | Reuse mentor list source. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD02/data-access/ad02-api.service.ts` | API #68 list caller | Reuse existing users list API client if possible. | `READ` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.spec.ts` | API #68 request expectations | Confirm query names/typing. | `READ` |
| `apps/study-client/src/app/features/admin/AD07/` | Detail route and ID handling | Navigate to a newly created course safely. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD07/pages/ad07-page.ts` | Route ID parsing and data load | Verify safe detail navigation after create. | `READ` |
| `apps/study-client/src/app/features/admin/AD07/pages/ad07-page.css` | Existing detail notice styles | Add a source-fit success status message. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD07/data-access/ad07-api.service.ts` | API #74 detail caller | Build a focused detail-route success feedback spec. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD08/` | Existing course form conventions and source-only fields | Reuse field semantics where supported. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD08/pages/ad08-page.ts` | Field parsing and form validation | Reuse current field semantics only. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD08/pages/ad08-page.html` | Course edit form fields | Confirm label/URL/price patterns. | `PLANNED` |
| `apps/study-client/src/app/features/admin/admin.routes.ts` | Course routes | Confirm dialog doesn't need a new route. | `READ` |
| `apps/study-client/src/app/shared/ui/` | Bounded filename inventory only | Identify reusable dialog/form controls. | `PLANNED` |
| `apps/study-client/src/app/shared/ui/admin-detail-page.css` | Existing Admin form/layout primitives | Reuse only matching styles. | `PLANNED` |
| `apps/study-client/src/app/core/constant/api.constants.ts` | API #68 and #73–#104 entries | Add the new WIRED POST descriptor. | `READ` |
| `apps/study-client/src/app/core/http/admin-api.service.ts` | GET/POST methods and authorization | Reuse the existing Admin transport. | `READ` |
| `apps/study-client/src/app/core/http/study-api.service.ts` | `StudyApiRequestOptions` and POST body transport | Confirm the request body option and `/admin/` endpoint handling. | `READ` |
| `apps/study-client/src/app/features/admin/admin-api-guards.ts` | Course/user response type guards | Validate API #68 mentor options and API #104 Course response. | `READ` |
| `apps/study-client/src/app/features/admin/admin-screen-state.ts` | Existing API error copy and query-state conventions | Preserve Admin API error communication in the create dialog. | `READ` |
| `apps/study-client/src/app/features/admin/admin-screen-renderers.ts` | Course row navigation mapping | Confirm existing precision-safe AD-07 route creation. | `READ` |
| `apps/study-client/src/app/features/admin/AD02/data-access/ad02-api.service.ts` | API #68 GET wrapper | Confirm reusable AdminApiService list pattern. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD02/pages/ad02-page.spec.ts` | API #68 request parameters | Verify role/status/page filter names. | `PLANNED` |
| `apps/study-client/src/app/features/admin/admin-api.models.ts` | Course and user response types | Define client request/response types. | `READ` |
| `apps/study-client/src/app/features/admin/admin-query-params.ts` | Admin query serialization helper | Preserve numeric mentor IDs and fixed page query. | `READ` |
| `apps/study-client/package.json` | Test scripts/runtime | Run focused Angular tests. | `PLANNED` |
| `apps/study-server/app/api/v1.py` | API #68/#73/#75/#88 sections and imports | Mount API #104 following current routing pattern. | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/` | Models/validation/query/view and tests; bounded inventory first | Confirm mentor list filters and reusable response projection. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/models.py` | User page and filter types | Confirm exact role/status/query response types. | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/validate.py` | Query validation | Confirm role/status accepted values. | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/query.py` | User SQL | Confirm mentor projection and active filter. | `READ` |
| `apps/study-server/app/modules/admin/api_68_admin_users_list/view.py` | API #68 orchestration | Confirm guard/query/response mapping. | `READ` |
| `apps/study-server/app/modules/admin/api_73_admin_courses_list/` | Models/validation/query/view | Reuse Course projection and list assumptions. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_73_admin_courses_list/models.py` | Course page and Course model | Confirm response projection to reuse. | `READ` |
| `apps/study-server/app/modules/admin/api_73_admin_courses_list/view.py` | Course mapper and transaction behavior | Confirm reusable course projection contract. | `READ` |
| `apps/study-server/app/modules/admin/api_73_admin_courses_list/query.py` | Current joined Course projection | Reuse existing course columns and mentor projection. | `READ` |
| `apps/study-server/app/modules/shared/course_catalog/models.py` | Shared Course response | Reuse the current Course response model. | `READ` |
| `apps/study-server/app/modules/shared/course_catalog/helpers.py` | `map_course` and exact price conversion | Reuse the source-backed course response mapper. | `READ` |
| `apps/study-server/app/modules/admin/api_75_admin_course_update/` | Models/validation/query/view and tests; bounded inventory first | Reuse current field validation only where source-backed. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_75_admin_course_update/models.py` | Request/response model declarations | Confirm field names and nullability. | `READ` |
| `apps/study-server/app/modules/admin/api_75_admin_course_update/validate.py` | Input validation | Inspect current field constraints and mentor policy gaps. | `READ` |
| `apps/study-server/app/modules/admin/api_75_admin_course_update/query.py` | SQL constants | Confirm columns and parameter names. | `READ` |
| `apps/study-server/app/modules/admin/api_75_admin_course_update/view.py` | Update flow only | Reuse established auth/transaction/projection conventions. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_75_admin_course_update/test_admin_course_update.py` | Relevant payload and response cases | Confirm current source behavior for fields. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_88_admin_quizzes_create/` | Models/validation/query/view patterns; bounded inventory first | Match an existing Admin create endpoint. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_88_admin_quizzes_create/models.py` | Request/response model | Match current Admin create model conventions. | `READ` |
| `apps/study-server/app/modules/admin/api_88_admin_quizzes_create/validate.py` | Input validation | Match safe validation/error mapping. | `READ` |
| `apps/study-server/app/modules/admin/api_88_admin_quizzes_create/query.py` | SQL constants | Match insert/returning style. | `READ` |
| `apps/study-server/app/modules/admin/api_88_admin_quizzes_create/view.py` | Auth, transaction and response flow | Match Admin POST pattern. | `READ` |
| `apps/study-server/app/modules/admin/api_104_admin_courses_create/models.py` | New API request/response models | Define the user-approved create contract. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_104_admin_courses_create/validate.py` | New API body validation | Enforce field, price and ID constraints. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_104_admin_courses_create/query.py` | New SQL constants | Check eligible mentor and persist course metadata. | `PLANNED` |
| `apps/study-server/app/modules/admin/api_104_admin_courses_create/view.py` | New API orchestration | Guard, lock mentor, insert, map and commit. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_104_admin_courses_create/test_admin_courses_create.py` | New focused regression cases | Verify auth, validation, mentor rules, response and rollback. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD07/pages/ad07-page.html` | Detail success feedback | Show the course-created confirmation after navigation. | `PLANNED` |
| `apps/study-client/src/app/features/admin/AD07/pages/ad07-page.spec.ts` | Detail navigation success feedback | Verify the one-time created state. | `CREATED_AND_VERIFIED` |
| `apps/study-server/infra/postgres/02_study_db.sql` | `courses` table declaration | Check existing fields before deciding on migration. | `NOT_FOUND` |
| `.agents/server-study/database.md` | Current schema/migration map | Locate the active checked-in schema evidence before choosing insert constraints. | `PLANNED` |
| `infra/postgres/study-server/` | Bounded SQL filename inventory only | Find the candidate Study schema referenced by AD-06 source notes. | `PLANNED` |
| `infra/postgres/study-server/DB.sql` | Course and user table declarations | Verify candidate columns, constraints, and defaults if present. | `READ` |
| `apps/study-server/` | Bounded `*.sql` filename inventory only | Locate any Study server migration that may define course constraints. | `PLANNED` |
| `apps/study-server/infra/` | Bounded `*.sql` filename inventory only | Locate the current candidate schema after the planned exact path was absent. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_68_admin_users_list/` | Relevant mentor filter cases | Verify API #68 selection query. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py` | Filter, auth and projection cases | Confirm API #68 behavior. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_73_admin_courses_list/` | Course page response fixtures | Preserve list projection expectations. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_73_admin_courses_list/test_admin_courses_list.py` | Existing course row fixtures | Confirm field/mentor response mapping. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_75_admin_course_update/` | Request validation helpers/cases | Reuse current accepted fields safely. | `PLANNED` |
| `apps/study-server/tests/modules/admin/api_88_admin_quizzes_create/` | Test pattern inventory | Locate existing Admin create test conventions. | `PLANNED` |
| `apps/study-server/pyproject.toml` | Test/lint commands | Run focused server verification. | `PLANNED` |
| `docs/lists/list_api.md` | Admin course API rows and API numbering | Document API #104 and its contract. | `READ` |
| `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md` | Summary, source trace and runtime limits | Carry forward prior audit. | `PLANNED` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Đăng ký API #104 tạo khóa học | Thêm descriptor và contract row không trùng API ID/path | Client registry and canonical API catalog agree on method, path, request and response. |
| Thêm API #104 lưu khóa học DRAFT | Implement Admin-authenticated create using existing course table and active mentor validation | Focused server cases confirm 201 Course response and safe failure paths. |
| Bật dialog tạo khóa học AD-06 | Add form, API #68 mentor selector and API #104 submit flow | Focused client cases cover validation, loading, success, failure and route behavior. |
| Đồng bộ DD/context cho API #104 | Update only affected AD-06 and Study API context pages | DD/context validator reflects current source and contract. |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `fix`
- selector_command: `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/select-worklogs.mjs --type fix --limit 3`
- selected: `.agents/worklog/2026-11-22/enable-admin-course-creation.md` (self-match), `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md`, `.agents/worklog/2026-11-22/fix-study-admin-overview-summary.md`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-22/fix-study-admin-courses-runtime-check.md`
    - carry_forward: API #73 is wired; the screenshot is a successful empty state, while course creation is absent and the button is disabled. The prior audit intentionally made no source change.
  - path: `.agents/worklog/2026-11-22/fix-study-admin-overview-summary.md`
    - carry_forward: Preserve prior AD-01/API #101 changes; fake-DB tests do not prove live schema or deployment.
- shortage: `none` (14 available; 3 selected with one self-match skipped)

## EXPECTED_BEHAVIOR

- Requirement: Admin can create a course from AD-06 in an accessible dialog.
- User-approved fields/policy: title required; description and thumbnail URL optional; price required; mentor required and must be `MENTOR/ACTIVE`; initial status is `DRAFT`; thumbnail is a URL, not an upload.
- User-approved UI: dialog on AD-06. On success, close dialog, show success and open AD-07 detail when the returned ID is JS-safe.
- Proposed API: #104 `POST /api/v1/admin/courses`, HTTP 201 `DESIGN_RESOURCE_CREATED`, returns the new Course projection.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Đăng ký API #104 tạo khóa học | 0% → 99% → removed | Registry, catalog and route agree on POST `/api/v1/admin/courses`; completed row removed per active-target rules. |
| Thêm API #104 lưu khóa học DRAFT | 0% → 99% → removed | Server route/module implemented; focused API #104 test module passes 6/6; completed row removed per active-target rules. |
| Bật dialog tạo khóa học AD-06 | 0% → 99% → removed | Dialog/#68 mentor selector/#104 submit and safe AD-07 handoff implemented; AD-06/AD-07 focused specs pass 10/10. |
| Đồng bộ DD/context cho API #104 | 0% → 99% → removed | AD-06 DD and Study API/Web contexts updated; validator baseline findings preserved; completed row removed per active-target rules. |

## CURRENT_BEHAVIOR

- Source/config: before this change AD-06 called read-only API #73 and the Add control had no create endpoint. Current API #73 remains list-only. The user-approved plan now wires API #104 through an ADMIN-protected server route, API #68 active Mentor options and the AD-06 dialog.
- Existing course storage supports `name`, nullable description/thumbnail, numeric price, mentor ID and status. The checked-in `infra/postgres/study-server/DB.sql` is a candidate schema, not proof of live DB compatibility.
- API #75 source accepts decimal strings and uses the same Course projection; API #104 requires a positive signed-int64 Mentor ID, exact ACTIVE/MENTOR check and starts new records at DRAFT.
- Focused API #104 tests passed 6/6; combined AD-06/AD-07 specs passed 10/10 after adding navigation-state coverage.
- Runtime wiring: source now includes POST #104 and client caller; authenticated browser, live API/DB and deployment remain `NOT VERIFIED`.

## SOURCE_TRACE

```text
AD-06 dialog -> AdminApiService.post -> Study Server API #104 -> Admin auth + mentor check -> courses INSERT -> Course envelope -> AD-07 detail
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Admin course creation before approved change | Prior source audit found no POST route and a disabled AD-06 button. | `NOT_FOUND` (resolved in this task) | Prior to change, user could not create a course. |
| API #104 deployment/schema | Focused fake-session tests and a checked-in candidate DDL only. | `UNVERIFIED` | Source behavior is implemented; live PostgreSQL acceptance is not established. |

## CHANGES

- Implemented Admin-authenticated API #104 POST route/module with strict request parsing, active Mentor lock-check, DRAFT insert, shared Course projection and caller-owned commit/rollback.
- Registered API #104 in the client API registry/catalog and added AD-06 service calls for #68 mentor paging and #104 create. The dialog validates and submits the form, presents pending/error feedback and routes safe created IDs to AD-07.
- Added AD-07 one-time success notice and focused navigation-state tests.
- Updated AD-06 eight-file DD, API catalog, server route/module/test context, Web Study context and Study contract index; no formal Study OpenAPI document exists beyond the placeholder.
- Context pages changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/apis/declared-routes.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/tests.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/project/contracts.md`.
- Assumptions: preserve all pre-existing dirty/untracked changes; use current candidate `courses` columns; do not deploy or mutate a shared/live database.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `uv run --project apps/study-server pytest apps/study-server/tests/modules/admin/api_104_admin_courses_create/test_admin_courses_create.py` | 6 passed; one upstream Starlette/httpx deprecation warning | `PASS` |
| `PATH=/home/daovanhung/.local/opt/node-v22.23.4/bin:$PATH npm test -- --include='src/app/features/admin/AD06/pages/ad06-page.spec.ts' --include='src/app/features/admin/AD07/pages/ad07-page.spec.ts'` (`apps/study-client/`) | 2 files, 10 tests passed; Angular test bundle built | `PASS` |
| `/home/daovanhung/.local/opt/node-v22.23.4/bin/node scripts/validate-agent-context.mjs` | Exit 1 as at baseline; the 77 structural findings are identical to the captured baseline (missing db-admin context, orphan skill resources and broken context links); source-drift sections remain | `BASELINE_INVALID; NO NEW STRUCTURAL FINDINGS` |
| `uv run ruff check app/modules/admin/api_104_admin_courses_create tests/modules/admin/api_104_admin_courses_create` (`apps/study-server/`) | Initial check found four E501 lines in the new validator; fixed to multiline form; rerun passed: All checks passed | `PASS` |
| `git diff --check` | No whitespace errors | `PASS` |

## HANDOFF

- Implementation and focused regression verification are complete. Live PostgreSQL schema, deployed API and authenticated browser runtime are not verified by this local checkout.
- The repository context validator remains invalid for the same structural findings recorded before this task; no new structural finding was introduced. Preserve unrelated dirty changes.
