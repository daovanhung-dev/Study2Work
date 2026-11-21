---
task_id: "2026-11-07-design-study-screen-ad12"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-34; AD-11 → AD-12; API #82; AD-13/#83 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-12

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 217; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; preserve original assets; trace auth/data/errors; keep Study Web UNWIRED unless editable source proves wiring; do not claim tests/runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve Admin permission, PII, lifecycle and live-schema blockers; do not infer fields/actions from prototype; source and fake-DB evidence are distinct.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep numeric handoff and source-backed mappings explicit; do not infer from mockup; preserve API-DD and runtime status distinctions.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-12 only in this session; create the screen plan before markers/annotation/DD; preserve source assets; provide ordered one-to-one markers, annotated image, A–F DD, per-event traces and explicit blockers; update screen/API inventory, global `dd_screens/PLAN.md`, and worklog; stop before AD-13.
- Inventory row 70: proposed `/admin/lessons`, AC-34/API #82, list lessons filtered by course/status/type and action to AD-13; expected `loading/empty/ready/error`; priority P1. AC-34 actor is Admin with lesson-management permission; postcondition covers update/status/delete through downstream APIs #84–#86.
- Catalog #82: `GET /api/v1/admin/lessons`; Bearer/Admin; optional `course:int64`, `status:string`, `type:string`; direct `ApiEnvelope<Lesson>` (singular); 200 plus 401/403/500. AC-34 flow opens list, queries lessons, then detail #83/operations #84–#86 and reloads list.

## CURRENT_BEHAVIOR

- Initial folder inspection found only `screen.png` (1600×1301, 275,097 bytes; SHA-256 `7f6557f79ccc48a98723fbf533330cd520f2840e780d9e17cd8f1533a49df6b1`) and `code.html` (20,130 bytes; SHA-256 `75a61628c416c0f7683c2dff234f5cb710b8449e5425c61ddd6572575d757f0d`).
- Prototype shows search, course/type/status selects, reset/refresh, seven-column lesson table, empty state, pagination, add-lesson CTA, static “API #82 active”, DB-sync, System Normal, SCORM/xAPI/DRM claims. No app request handler or data binding is source-backed; links are hash placeholders, controls have no event handler, the empty-state list refresh is disabled, and the source has only Tailwind configuration scripts.
- Study Web editable route/source/package/client remains absent in the current app tree; only docs/assets, ignored build/dependency artifacts are present. Runtime is `UNWIRED` / `NOT VERIFIED`.
- API #82 is wired locally. It checks shared JWT role `ADMIN` before query parsing/DB access, then parses optional signed-int64 `course`, rejects any supplied `type` with 422 `UNSUPPORTED_FILTER`, and binds exact optional `course_id`/`status`. SQL reads candidate legacy BIGINT `lessons`, excludes `status='DELETED'`, orders `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`; no join/count/page/mutation. Response is unpaginated `ApiEnvelope<Lesson[]>`; empty is 200 `data: []`.
- Reusable Lesson fields are `id`, `course_id`, `title`, nullable `content`, nullable `video_url`, `order`, `status`; query maps `name→title`, `sort_order→order`. No lesson type/code/course title is returned. The legacy `lessons` DDL permits nullable `course_id`, `sort_order`, `status` even though the response model requires values; malformed/null required projection returns safe 500 + rollback. Checked-in DDL and fake DB test rows do not establish live schema/deployment.
- API #82 DD is `Draft — Needs Confirmation`; it records array/cardinality, filter semantics, ordering, 422s, no pagination and tombstone filtering as DERIVED/local. AC-34's dedicated lesson-management permission is not enforced by the shared `ADMIN` guard.
- API #82 test source reviewed, not run: `apps/study-server/tests/modules/admin/api_82_admin_lessons_list/test_admin_lessons_list.py`. It covers fake-session auth order, signed-int64 course parsing, exact filters, unsupported type, empty array, null required projection rollback, query failure rollback, OpenAPI. Test fixtures are fake rows; no PostgreSQL/live-schema proof.

## SOURCE_TRACE

```text
Expected: Admin with lesson-management permission → AD-12 GET #82
          → choose Lesson → AD-13/#83 → optional AD-14/#84/#85/#86
          → AC-34 reload list.
Current: no Study Web caller → #82 shared ADMIN guard → signed-int64 course
         + explicit rejection of any supplied type → exact course/status SQL
         on legacy BIGINT lessons candidate → Lesson[]/empty array; read-only.
```

Sources reviewed: root objective, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/template and selected worklogs; `.agents/project/INDEX.md`/dependencies/contracts; web-work Study Web router/index and design guide; server-study entry/index, module/runtime/security/database/test context; `apps/study-client/docs/list_screen.md` rows 70/AC-34 flow/API reverse row 082; `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` and `AC_04_ADMIN_MANAGEMENT.drawio`; `docs/lists/list_api.md` #82; API #82 DD Overview/Request/Response/Open Questions; `apps/study-server/app/api/v1.py` #82/#83 routes; #82 models/validator/query/view, reusable API #09 Lesson model, focused test source, checked-in legacy DDL. Registry confirms no canonical UI-only DD skill; API skill `createDD-markdown` excludes this boundary.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API response shape | Catalog/AC says singleton `ApiEnvelope<Lesson>`; local #82 returns `ApiEnvelope<Lesson[]>`. | `DISCREPANCY` | Collection behavior is a local DERIVED fallback; owner must reconcile catalog. |
| Filters | Mockup has keyword, course slugs, type values and active/draft/hidden; local #82 has no keyword, needs int64 course, rejects any supplied type with 422, exact status string. | `DISCREPANCY` | Do not invent course ID mapping, type mapping or status aliases. |
| Pagination | Mockup shows `0/0` and Previous/Next; #82 has no page/size/count and returns all matches. | `DISCREPANCY` | Counter/paging cannot map to current response. |
| Row fields/actions | Mockup columns include course, format and actions; response only has numeric `course_id` and no `type`/code/course name. Add lesson has no create API in AC-34/#82–#86. | `BLOCKER` | Do not fabricate missing columns or create endpoint; detail handoff uses numeric `Lesson.id` to #83 only. |
| Access/source/schema | AC-34 says lesson-management permission; current guard only checks `ADMIN`. BIGINT vs V1-PILOT UUID models differ; required projections can be null in legacy DDL. | `OPEN / NOT_VERIFIED` | Authorization, live schema and malformed legacy row behavior remain unapproved/unverified. |
| Study Web and prototype claims | No editable Study Web route/client; static HTML shows DB sync, API active, system health, SCORM/xAPI/DRM without matching #82 data/behavior. | `UNWIRED / STATIC_ONLY` | No current runtime claim; do not describe copy as measured behavior. |

## CHANGES

- `apps/study-client/docs/screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_PLAN.md`: detailed pre-work plan saved before annotation/DD; execution/static-audit checklist completed.
- `apps/study-client/docs/screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12_markers.json` and `AD-12_markers.svg`: 42 ordered markers with source-image coordinates and in-bounds circle strokes.
- `apps/study-client/docs/screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/screen_annotated.png`: 3200×2602 composite rendered 2× over a resized copy; original `screen.png` unchanged.
- `apps/study-client/docs/screen_stitch/05_admin/AD-12_danh-sach-bai-hoc-quan-tri/AD-12.md`: A–F DD with 42 element rows and EV-01…EV-09; catalog/source discrepancies and blockers remain explicit.
- `apps/study-client/docs/list_screen.md`: AD-12 source status `D→R`; DD remains blocked with current query, access, schema and wiring limitations.
- `apps/study-client/docs/list_screen.md` reverse API index: #082 `D→R` from route/module/query/model/test-source evidence.
- `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`: AD-12 row and checkpoint updated to 65/83 core artifact sets, with AD-13 identified as the next separate screen session.
- CONTEXT_UPDATES: none. Context pages and registries were not changed.
- Assumptions added: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective reread; docs selector READY 3/217; exact selected AD-01/02/03 worklogs reviewed. | VERIFIED |
| Source and contract trace | AC-34, API #82 catalog/DD, #82 route/module/query/model/test source, legacy DDL candidate, API #83 route, static screen/HTML, Study Web design and registry reviewed. | VERIFIED |
| Source preservation | SHA-256 `screen.png`=`7f6557f79ccc48a98723fbf533330cd520f2840e780d9e17cd8f1533a49df6b1`; `code.html`=`75a61628c416c0f7683c2dff234f5cb710b8449e5425c61ddd6572575d757f0d`; match preflight. | VERIFIED |
| Marker/DD/image static audit | 42 JSON entries and SVG groups in order; IDs, coordinates, text labels and circle/stroke bounds agree; 42 C rows biject; JSON/XML parse; all DD relative links resolve; source 1600×1301, annotated 3200×2602; annotated image visually inspected. | VERIFIED |
| Screen coverage/checkpoint | 83 unique inventory IDs match 83 asset folders; 65/83 have all four core artifacts after AD-12. | VERIFIED |
| Whitespace | Authored AD-12 files checked for trailing whitespace; `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` returned clean. | VERIFIED |
| Application tests/runtime | Not run; fake-DB test source was reviewed only. | NOT_RUN |

## HANDOFF

- AD-12 result: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED` (`UNWIRED`). API #82 DD remains `Draft — Needs Confirmation`.
- Open blockers: catalog singular vs local collection, course slug/int64 option mapping, unsupported type filter, search/status mapping, pagination, unsupported table fields/actions and Add route, lesson-management permission, legacy nullability/live schema, and missing Study Web route/client.
- Next screen: AD-13 in a separate session. This session stopped after AD-12.
