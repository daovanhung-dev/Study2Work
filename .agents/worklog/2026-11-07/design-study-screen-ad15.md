---
task_id: "2026-11-07-design-study-screen-ad15"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-35; API #87; AD-15 → AD-16/17/18 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-15

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 220; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; preserve assets; trace catalog/AC against route/query/response/tests; retain Study Web `UNWIRED` and do not claim unrun tests/runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer search/filter/action semantics from mockups; distinguish local backend behavior from Draft API DD and fake DB evidence; preserve authorization, lifecycle and schema blockers.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve identity/navigation boundaries; current source outranks docs; test source alone does not prove live schema or deployment; UI-only DD has no canonical skill.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad14.md` — next screen is AD-15; keep one-screen-per-session boundary; do not start AD-16.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-15 only in this session. Read the objective and routed context; inspect AD-15 assets, row 73, AC-35, API #87 and relevant source/tests. Write `AD-15_PLAN.md` before creating marker data, annotation or screen DD; preserve original assets; create an ordered one-to-one marker map and annotated image; write A–F DD with traceable events, API/error/state/navigation details and explicit blockers; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; stop before AD-16.
- Objective requires each Screen ID to be handled in a separate session with source-backed, implementable screen DD. `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED` are separate statuses; do not treat them as interchangeable.
- Inventory row 73 and AC-35 expect Admin quiz management at `/admin/quizzes`; AC-35 requires quiz-management permission and runs API #87 before a Create/Update/Delete/Statistics decision (#88–#91). The catalog directly declares `ApiEnvelope<Quiz>` and optional `course:int64`, `status:string`, `page:int32`; current source must be compared before using the list response or filters.
- No quiz field, filter enum, course mapping, action result, or runtime route may be inferred from the prototype. Keep API #87's Draft contract separate from current local fallback behavior.

## CURRENT_BEHAVIOR

- Source/config: At inspection start, AD-15 folder contained only `screen.png` (1600×1394; SHA-256 `a58cc4433342fe13441b337f2ca287a8b6fde354180ff73ff488f9d8d235401a`) and `code.html` (20,852 bytes; SHA-256 `d8b6e43ee2e9832bb5bbfd13ae6a7bd802877ecc2207ad3fb43db6ced7878473`). HTML is static: search/course/status controls have no data handlers; course values are slugs and statuses are lowercase `draft/active/closed`; create and advanced-filter buttons are disabled; pagination is disabled; links use `#`. The two refresh buttons only animate their icons for 800 ms and do not fetch data. Study Web currently has docs/assets, `dist/index.html` and dependency artifacts but no editable app source, package manifest, router or API client; the compiled artifact has no `/admin/quizzes` or API #87 string. UI status `UNWIRED`.
- API #87 catalog is GET `/api/v1/admin/quizzes`, Bearer JWT/Admin, no body, optional query `course:int64`, `status:string`, `page:int32`, direct `ApiEnvelope<Quiz>`, 200/401/403/500. The route is locally composed and passes raw values to `get_admin_quizzes`; the shared ADMIN guard precedes query validation/DB. Local source validates signed-int64 `course` and signed-int32 page >=1 (invalid -> 422), keeps status text unchanged, queries legacy BIGINT `quizzes` count + page with exact optional filters and unconditional `DELETED` exclusion, size 20/page 1/`id ASC`, maps metadata-only Quiz rows with `questions=[]`, returns `ApiEnvelope<Page<Quiz>>`, returns 200 for empty/late pages, and performs no commit. Query/count/projection failures return safe 500 and rollback. These local page/filter/tombstone/error choices are DERIVED; the API #87 DD remains `Draft — Needs Confirmation`.
- Current list projection exposes `id`, `course_id`, `title`, optional `duration_minutes`, `passing_score`, and `questions=[]`; it does not expose a quiz code, course title, question count, or status. Catalog `ApiEnvelope<Quiz>` conflicts with AC-35/list intent and local `Page<Quiz>`. The screenshot's search-by-name/code is unsupported; course values do not match numeric `course`; status options lack an approved mapping; its 0/0 page counter conflicts with local page 1 and `total_pages=0` for an empty result. Legacy BIGINT quiz tables are only checked-in candidates; V1-PILOT uses UUID assessments/options, and live schema/deployment is unverified. Legacy `course_id`/`passing_score` nullable values can fail the required local response projection.
- Runnable tests: API #87 focused test source was reviewed. The API DD verification report records a previous 20-test focused pass, 93 linked regressions and 1113 full-suite tests at that checkpoint; tests use fake DB sessions and do not prove live schema/deployment. No tests were run in this screen-design session.
- Runtime wiring: Study Server locally composes API #87. Study Web screen route/caller/client remains `UNWIRED`; no runtime behavior is verified.

## SOURCE_TRACE

```text
Expected: AC-35 Admin with quiz-management permission opens `/admin/quizzes` → GET #87 list → choose Create (#88), Update (#89), Delete (#90) or Statistics (#91) → display operation/statistics result; AD-16/17/18 are related destinations.
Current: no Study Web caller → composed Study Server route → shared ADMIN auth → raw query parsing → legacy BIGINT count/page SQL → metadata-only `Page<Quiz>` response; no commit on GET. Direct catalog singleton response, source Page fallback, screen columns/filters, permission and live schema remain discrepant or unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response cardinality / projection | Catalog declares `ApiEnvelope<Quiz>`; AC-35 and `page` imply a collection; local source returns `ApiEnvelope<Page<Quiz>>` with metadata-only `questions=[]`. It lacks screen course title, question count and status. | `DISCREPANCY / BLOCKER` | Owner must approve list response and field mapping before implementation. |
| Search and filters | Prototype search by name/code is not in #87; course option values are slugs vs numeric `course:int64`; status options are lowercase draft/active/closed while backend applies exact raw text without enum validation. | `DISCREPANCY / BLOCKER` | Do not send unsupported search or invent option/ID/status mappings. |
| Authorization and schema | AC-35 requires quiz-management permission; local source checks only shared `ADMIN`. Legacy BIGINT DDL conflicts with V1-PILOT UUID assessment model; live schema is unverified. | `OPEN / BLOCKER` | Permission mapping, physical schema and lifecycle/status policy need confirmation. |
| UI wiring and static claims | No editable Study Web source/router/client; refresh only spins 800 ms; `SYSTEM NORMAL`, scoring readiness, security V3 and “not synced” copy have no API #87 source. Mockup also differs from Study Web visual target. | `UNWIRED / DESIGN DISCREPANCY` | No frontend or runtime claim; static operational copy must not be presented as measured backend state. |
| Page/error state | Prototype shows `0/0`; local page response is one-based with `total_pages=0` on empty. Catalog errors are 401/403/500; local invalid course/page adds 422. | `DISCREPANCY / DERIVED` | Keep page/error behavior tied to approved response contract; do not call empty results unsynced. |

## CHANGES

- Created `AD-15_markers.json` and `AD-15_markers.svg` with 50 markers, `screen_annotated.png` at 3200×2788, and `AD-15.md` with A–F, 50 element rows and EV-01…EV-12. Kept source `screen.png` and `code.html` unchanged. Marker #39 was moved clear of the `0` page chip after crop review.
- Updated `list_screen.md` row 73 with local API #87 source status and explicit contract/UI blockers; reverse index #087 changed D→R because route/module/query/model/test source is locally composed. API DD #87 remains Draft. Updated global plan AD-15 row and 68/83 checkpoint.
- Files changed: `apps/study-client/docs/screen_stitch/05_admin/AD-15_danh-sach-bai-kiem-tra/AD-15_PLAN.md`, `AD-15_markers.json`, `AD-15_markers.svg`, `screen_annotated.png`, `AD-15.md`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` read; root router, `.agents/AGENTS.md`, context map, worklog contract/template reviewed; selector READY 3/220; AD-01, AD-02, AD-03 selected worklogs read. | VERIFIED |
| AD-15 scoped inspection | Inventory, source assets/HTML, AC-35 index/diagram, API catalog and Draft DD #87, route/module/query/model/test source, local DDL and Study Web tree/design target reviewed. | VERIFIED_SOURCE_REVIEW |
| AD-15 static artifact audit | `screen.png` 1600×1394 and `screen_annotated.png` 3200×2788; source hashes unchanged (`screen.png` `a58cc443…401a`, `code.html` `d8b6e43e…8473`). JSON/SVG have 50 sequential, unique, bounded markers, no overlaps; SVG parses; 50 DD §C rows match JSON coordinates; A–F and EV-01…EV-12 exist; 5 relative links resolve; inventory/folders 83/83; core artifact set 68/83; final image visually inspected. `git diff --check` on tracked inventory/global plan is clean; no added tracked lines have trailing whitespace, and generated/updated text artifacts are clean. Full-file baseline comparison found pre-existing trailing whitespace on unchanged `list_screen.md` lines 3–6. | VERIFIED |
| Application tests/runtime | Not run; screen stays `UNWIRED`, runtime not verified. | NOT_RUN |

## FINAL_STATUS

- AD-15 screen: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Remaining blockers are list response shape/projection, missing search/course/status mappings, AC-35 permission policy, live schema/deployment and Study Web wiring.
- AD-15 documentation/artifact review is complete. API #87 DD remains Draft. No application tests or runtime were run.

## HANDOFF

- Remaining blockers: owner decision on response cardinality/fields and filter mappings, fine-grained permission, live schema/deployment verification, and Study Web route/client implementation.
- Next screen in a separate session: AD-16. Do not start it in this session.
