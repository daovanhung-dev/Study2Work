---
task_id: "2026-11-07-design-study-screen-ad06"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AD-06 Study Web course administration ↔ API #73 / AC-32; verify handoff to AD-07..AD-09"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 211; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current behavior; inspect Study Web wiring; do not infer KPI, identity, route or data behavior from static mockups; distinguish API catalog from source.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep AC permission separate from local ADMIN claim; trace route through filters/query/response/tests; do not invent role/status enums or actions; retain live schema and PII policy blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve numeric ID and AC-31 handoff; keep audit/PII/lifecycle policy explicit; tests and fake DB do not prove deployment/runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-06 only in this session; read current inventory and cross-scope evidence; write `AD-06_PLAN.md` before marker map, annotation, or DD; preserve original assets; create ordered one-to-one markers and annotated image; author A–F screen DD; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation blocking, and runtime verification.
- Inventory row 64 defines AD-06 as the Admin course list at proposed `/admin/courses`, AC-32 / API #73, entered from Admin navigation and linked onward to AD-07. It proposes search, mentor/status filters, detail navigation and status-management flow; these are design requirements to compare against current source.
- Required deliverables are an individual plan, numbered element map, annotated image, A–F DD, updated inventory/reverse API source status/global plan and completed worklog. `screen.png` and `code.html` must remain byte-identical.

## CURRENT_BEHAVIOR

- Source folder initially contains only `screen.png` and `code.html`; the original PNG is 1600×1514. SHA-256 before authoring: PNG `9a053f394278f68f7ebd129e09b5c6455236d891aa822caf10ac9905156f28c0`; HTML `f7be6a5072ba3438a27350ff1429aee208782b7c80c333dd998d6642fc1013f4`.
- The static HTML has 9 `href="#"` anchors, 8 buttons, a text input and two selects. Only Reset has a JavaScript listener; it clears search and restores status/mentor to `all`. There is no fetch/XHR or API handler. Search, export, add, refresh/manual-sync, pagination and navigation are not wired.
- The mockup shows four hard-coded zero KPI cards; search for name/code/instructor; lowercase status options; an “all mentors” select; a disabled category badge; an empty table with columns code/name/instructor/fee/status/lesson count/actions; empty-state copy, disabled refresh, sync-manual link, static API path, result count/pagination and a moderation-governance banner.
- Study Web remains `UNWIRED`: editable app source, package manifest, router and client are absent; ignored `dist` contains only a root route and is not provenance for AD-06. Target design guidance is not runtime evidence.
- API #73 has a local route/module/model/validation/query/view/test source. The current source uses a shared `ADMIN` JWT role guard before raw query validation/DB access; the AC-32 fine-grained course-management permission mapping is not independently established. `status` is exact-match raw string; `mentor` and `category` parse signed int64; valid category is rejected with 422 because no source-backed relation exists; `page` is 1..2,147,483,647, default 1, fixed size 20 and `courses.id ASC` ordering.
- The read-only count and list share status/mentor predicates, join `courses` to `users`, and return `Page<Course>` (`id`, `title`, nullable description/thumbnail, exact decimal-string price, status, mentor id/name/avatar) with pagination. Search, course code, lesson count, KPI aggregates and category are not returned. Empty and out-of-range pages return 200 with empty `items`; an out-of-range page retains `total`. Missing mentor rows or invalid query/projection causes safe errors/rollback.
- API #77 locally soft-deletes by setting course `status='DELETED'`; API #73 query has no status exclusion, so a deleted course can remain visible in the list if unfiltered. Status vocabulary/transitions are not approved by that observation.
- API test report dated 2026-11-01 records 20/20 focused HTTP requests on a temporary schema/fixture branch passing after explicit nullable SQL casts, plus 178 focused tests and the full suite at that time. This is isolated test-environment evidence, not production schema/deployment or current frontend runtime verification. API DD #73 remains Draft — Needs Confirmation.
- AC-32 sequence is GET #73 list → GET #74 detail → #75 update / #76 status / #77 delete → reload list. Inventory purpose mentions status edit, but direct status action from an AD-06 row is unresolved; screen-to-action target stays through AD-07/AD-09. Search and mockup-only controls do not map to #73. Course category relation is absent from checked-in legacy DDL; V1-PILOT is a different model and must not be substituted. Live schema is unverified.
- Screenshot palette/type differs from target `.agents/web-study/design.md`; visual alignment remains an implementation task after Study Web is wired.

## SOURCE_TRACE

```text
Expected: list_screen.md row 64; AC-32 in AC_04_ADMIN_MANAGEMENT.drawio; API V1 catalog #73; route-level Admin course-list sequence and target Study design guidance.
Current UI: AD-06 screen.png + code.html; Study Web source/root and .agents/web-study/design.md. Prototype is static, and Study Web is UNWIRED.
Current API: app/api/v1.py #73 -> modules/admin/api_73_admin_courses_list/{models,validate,query,view}.py -> shared course_catalog mapper/model; local tests and 2026-11-01 HTTP test report. API #77 query supplies the DELETED marker behavior.
Persistence: infra/postgres/study-server/DB.sql legacy candidate; categories have no course FK. V1-PILOT DDL is a separate model; live schema/deployment not verified.
Cross-scope contract: AC-32 permissions and list→detail/status/update/delete sequence; API #73 / #74 links AD-06 to AD-07 by numeric Course.id. Do not author AD-07 here.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Study Web route/action runtime | No editable source/package/router/client; prototype only has a Reset listener. | UNWIRED | Screen cannot be described as implemented; all controls needing backend/navigation remain design-only. |
| Search by name/code/instructor | Mockup advertises search; API #73 has no search query or caller. | BLOCKER | Search cannot be specified as a working AD-06 feature until contract/source is approved. |
| Course code and lesson count columns | Mockup includes them; API #73 response has neither field. | BLOCKER | Do not map `id` to “course code” or invent a lesson-count query. |
| Four KPI cards | Mockup hard-codes zero; #73 only returns filtered page `total`, without status/mentor aggregates. | BLOCKER | No truthful aggregate mapping or filter semantics for cards. |
| Status selector and deleted rows | Mockup has lowercase draft/pending/published/archived; #73 exact-matches an unvalidated raw string; #77 writes `DELETED`, and #73 does not exclude it. | BLOCKER | Approved status vocabulary/casing and visibility/transition policy required; do not use mockup values as enums. |
| Mentor selector | #73 accepts numeric int64 mentor filter, but supplies no option list; mockup only shows “all”. | OPEN | Need approved mentor-option source and label/value mapping; do not infer complete choices from one page. |
| Category filter | No course-category FK in checked-in legacy DDL; valid category query is explicitly rejected 422 in #73 source. | BLOCKER | Keep locked; requires data relation and API/contract decision. |
| Export/add/sync/manual/policy controls | Mockup buttons/links have no handler; #73 only reads list and AC-32 has no create/export/manual-sync API. Governance sentence is not established by #73. | BLOCKER | Retain as unresolved prototype-only controls; do not map to unrelated export or approval APIs. |
| API #73 local test evidence | 2026-11-01 report: focused requests on temporary test branch returned 200 after nullable-cast fix; DD remains Draft. | SOURCE_BACKED; RUNTIME ENVIRONMENT LIMITED | Does not establish live database/deployment or frontend runtime; list screen status is R, screen runtime remains unverified. |
| Status action path | Inventory purpose mentions status edit; AC-32 goes through #74 before choosing #76. | DISCREPANCY / OPEN | No direct list-row status action specified; retain AD-07 handoff. |
| Visual system | Screenshot differs from target Study guide palette/type. | DESIGN DISCREPANCY | Do not treat prototype visual tokens as canonical or runtime evidence. |
| Admin permission mapping | Local source checks shared role `ADMIN`; AC-32 precondition names course-management permission. | DERIVED / OPEN | Owner must confirm whether ADMIN claim is sufficient for this screen. |

## CHANGES

- Files changed: `AD-06_PLAN.md`, `AD-06.md`, `AD-06_markers.json`, `AD-06_markers.svg`, `screen_annotated.png`; `list_screen.md` AD-06 row and #073 reverse source status; `dd_screens/PLAN.md` AD-05/AD-06 rows and AD-06 checkpoint; this worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: `/admin/courses` remains a proposed route; #73 behavior describes current checked-in source and Draft API contract, not approved business policy; direct status action from list remains unresolved.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`, selected 3/211; all three selected docs worklogs read in full. | VERIFIED |
| Objective file | Read `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` before continuing. | VERIFIED |
| Source hashes | `screen.png` SHA-256 `9a053f394278f68f7ebd129e09b5c6455236d891aa822caf10ac9905156f28c0`; `code.html` SHA-256 `f7be6a5072ba3438a27350ff1429aee208782b7c80c333dd998d6642fc1013f4`, matching initial hashes. | VERIFIED |
| Image dimensions / visual review | Original `1600×1514`; annotated PNG `3200×3028`; generated from 44 markers and opened/checked for label obstruction. | VERIFIED |
| Marker/element audit | JSON valid; markers 1–44 sequential/unique/in-bounds; SVG contains matching 44 groups/coordinates/labels; DD C table has exactly 44 rows. | VERIFIED |
| Local markdown links | All relative links in AD-06 DD resolve to local files. | VERIFIED |
| Inventory/core artifact count | 83 unique inventory IDs and 83 matching screen folders; 59/83 have all four core files after AD-06 (24 incomplete). | VERIFIED |
| Whitespace | `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` plus custom trailing-whitespace check for new AD-06 and worklog files. | VERIFIED |
| Application tests/runtime | Not run in this session; existing API report was read only. | NOT_RUN |
| Agent-context validator | Not run; no `.agents` context page/registry changed. | NOT_APPLICABLE |

## HANDOFF

- Completion: AD-06 artifacts and static audit complete. DD remains `BLOCKED`; implementation remains `BLOCKED`; Study Web runtime `NOT VERIFIED`.
- Remaining blockers: AC-32 Admin permission mapping; status enum and `DELETED` visibility; search/category/mentor options/data/KPI/course fields; export/create/sync/governance controls; Study Web source/router/API wiring and live schema/deployment.
- Next owner/action: process AD-07 in a separate session; no additional Screen ID was authored in this session.
