---
task_id: "2026-11-07-design-study-screen-gs04"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-04 curriculum tab ↔ GS-03 course-public gate, AC-05/F02 orchestration, API #08/#09 and ST-10 access boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-04

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 260; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; preserve source assets; distinguish local source from Draft/API and live schema; do not imply UI runtime or test results.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Trace contracts and current source independently; UI-only DD has no canonical skill; preserve UNWIRED and implementation blockers without inventing behavior.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use only explicit identity/data handoffs; distinguish source-backed local APIs from Draft DD and deployment; preserve static prototype semantics and test/runtime status.
- additional_recent_screen_log: `.agents/worklog/2026-11-07/design-study-screen-gs03.md` read for the immediate GS-03 → GS-04 handoff and current API #08/#09 discrepancies.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Handle GS-04 only in this session; review/write `GS-04_PLAN.md` before editing DD or annotations; preserve original assets; ensure ordered one-to-one markers, source-traced DD events/API/states/navigation, inventory/global-plan checkpoint and worklog; distinguish DD readiness, implementation block and runtime verification.
- Current inventory row 11 proposes `/courses/:courseId?tab=curriculum`, AC-05, API #09, links GS-03/ST-10, and loading/empty/ready/error states. F02 says #08 course gate then lazy #09; GS-04 row mentions reuse of #08 from cache. API catalog declares `course_id:int64`, `ApiEnvelope<Page<Lesson>>`, and 200/404/500. Verify current row and sources before relying on this.

## CURRENT_BEHAVIOR

- Assets: GS-04 folder contains source `screen.png` and `code.html`, derived `screen_rendered.png` and `screen_annotated.png`, JSON/SVG marker map, plan and DD. Original screenshot is nearly blank; HTML-derived render shows the actual static empty-like page. The annotation has 10 gutter markers and was visually reviewed; source assets were preserved.
- API #09: route accepts `course_id:str`; `validate_course_id` calls shared `parse_integer`; Q1 gates PUBLISHED course, Q2 lists PUBLISHED lessons ordered by `sort_order ASC, id ASC`; response maps `Lesson{id,course_id,title,content?,video_url?,order,status}` into one page. Empty items return HTTP 200, `total_pages=0`; invalid/missing/unpublished returns 404; SQLAlchemy query or mapping errors return safe 500 (query exceptions roll back). Route, validator, query, model, view and focused fake-session test source were read; tests were not run.
- API #09 discrepancy: catalog says `course_id:int64`, but the route accepts `str` and `parse_integer` checks integer syntax only (optional sign/digit separators, Python digit ceiling), not signed-int64 or positive range. Focused tests cover an ordinary ID and non-integer input, not range boundaries.
- API design/security: API #09 DD is `Draft — Needs Confirmation`; it calls the current PUBLISHED filter a design assumption. Current public response contains `content` and `video_url`, but no preview/access flag. Do not expose/open lessons or media from GS-04; ST-10 #22–#24 is a separate Student path and those APIs are declared, not current routes.
- Schema: legacy BIGINT `DB.sql` matches API #09 queried columns but has no preview flag; V1-PILOT `02_study_db.sql` uses UUID/versioned lessons (`title/summary/position/estimated_minutes/is_preview`) and different relations. `.agents/server-study/database.md` marks live schema unverified; current API #09 does not query the V1-PILOT model.
- Orchestration/handoff: inventory wants #08 cache reuse → #09; F02 says lazy-by-tab; AC-05 shows #09 eagerly after #08. Cache key/freshness/miss/direct-entry rules are not specified. Preserve the same `courseId` from GS-03; do not turn ST-10's access/start/content path into a Guest lesson action.
- Study Web: `.agents/web-work/study/INDEX.md` reports `UNWIRED`; current `apps/study-client/` tree shows docs/assets and ignored `dist`, no editable source or package manifest.

## SOURCE_TRACE

```text
Expected: GS-03 provides the same `courseId` → Guest curriculum tab → #09 after course-public gate → ordered lesson list or separate empty state; private lessons are not opened by Guest. F02 lazy tab load conflicts with AC-05 eager sequence; inventory also asks to reuse #08 cache.
Current: Study Web has no caller/router. Study Server #09 source independently gates PUBLISHED course then lists PUBLISHED lessons and exposes content/video fields in a public response; API DD leaves that visibility rule unapproved. Empty is HTTP 200; error paths are 404/500. Fake-session test source exists; no tests run. Checked-in DDL models differ and live schema is unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #09 local behavior | Route, validator, query, model/view and test source reviewed; PUBLISHED course/lesson filter, deterministic order, empty 200, 404/500. | SOURCE_BACKED LOCALLY; tests not run | Do not infer deployed DB/schema or access policy. |
| API #09 visibility/access | API DD says PUBLISHED filter is an assumption; current public payload contains content/video_url without preview/access field. | DISCREPANCY / BLOCKER | Keep Guest lesson open/media behavior blocked. |
| API #09 ID type | Catalog says int64; route accepts str; parser has no int64/positive bound; boundary tests absent. | DISCREPANCY | Owner must clarify validation and oversized-ID mapping. |
| API #09 storage schema | Legacy BIGINT and V1-PILOT UUID/versioned DDL differ; live schema unverified. | DISCREPANCY / NOT VERIFIED | Do not infer preview fields or schema used by runtime. |
| Orchestration/cache | Inventory #08 cache reuse, F02 lazy #09, AC-05 eager #09; no cache/miss contract. | DISCREPANCY / OPEN | Product/BE must settle before implementation. |
| Study Web | Registered subcontext says `UNWIRED`; app source/package absent. | UNWIRED | No route/runtime claim. |
| Visual assets/markers | Original screenshot near blank; HTML-derived static render readable; 10 markers point to existing elements without occlusion. | VERIFIED | Preserve originals and identify rendered image as derivative. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_PLAN.md`, `GS-04.md`, `apps/study-client/docs/list_screen.md` (GS-04 row), `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (GS-04 row/checkpoint), this worklog. No image or application source changed.
- CONTEXT_UPDATES: none; no registered context page was made inaccurate by this documentation update.
- Context pages changed: none.
- Assumptions: No runtime behavior inferred from static HTML, source tests, Draft API DD or checked-in DDL.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; all selected docs worklogs read individually. | VERIFIED |
| Worklog contract | README and TEMPLATE reviewed; current worklog created with preflight record. | VERIFIED |
| Router/context/skill routing | Current `.agents` router, context map, project index, Web/Study Web and Study Server scope entries/indexes, module index, registry and project dependency/contract/test snippets reviewed. Registry excludes UI-only DD from canonical DD skills. | VERIFIED |
| GS-04 plan and source bundle | Existing plan and DD read; dated re-audit plan inserted before DD/inventory edits; source PNG/HTML/render/annotation visually inspected. | VERIFIED |
| API/AC/schema handoff trace | Inventory, F02/F04, AC-05, API catalog/#09 Draft DD, route/validator/query/model/view/test source, legacy and V1-PILOT DDL, server database context, GS-03 and ST-10 handoffs reviewed. Test source only; no tests/runtime/live DB run. | VERIFIED (source/document review) |
| Static asset/marker audit | Source hashes and image dimensions verified; all eight bundle files present; 10 ordered unique markers map to 10 DD rows and 10 SVG labels, stay within canvas, and SVG embeds the exact rendered PNG; all six events specify input/trigger, processing and output; local links resolve; 83 inventory IDs match tracker rows and folders. | VERIFIED |
| `git diff --check` | `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` exited 0 after edits. | VERIFIED |

## HANDOFF

- Remaining blockers: API #09 published-only visibility remains an unapproved assumption while public response contains content/video_url; int64 parser mismatch; legacy/V1-PILOT/live schema; missing loaded-list/preview/error design; #08 cache and AC/F02 orchestration/direct-entry; Study Web UNWIRED.
- Next Screen ID: GS-05, for a separate session. GS-04 static audit is complete; keep DD and implementation blocked, runtime not verified.
