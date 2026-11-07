---
task_id: "2026-11-07-design-study-screen-sh06-reaudit"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-06 route/resource 404 state ↔ Study API #08 and AC-05; safe navigation to SH-01/GS-01"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study SH-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 255; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; do not infer routes or data from mockups; trace API and effects; keep Study Web `UNWIRED`; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Distinguish catalog/AC from current source; do not invent filter/business behavior; tests/fake DB do not establish live deployment/schema.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep server source, draft contract, implementation and runtime status separate; preserve PII/privacy and route gaps.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh06.md` (supplemental, screen-specific)
    - carry_forward: SH-06 has current design assets and 22-marker/10-event artifact set; source #08 returns 404 for invalid/missing/unpublished, 500 for internal errors and no 403 branch; preserve AC-05 404/403 discrepancy and UI/source gaps.
  - path: `.agents/worklog/2026-11-05/design-study-screen-sh06.md` (supplemental, screen-specific)
    - carry_forward: API #08 success is singleton `Page<Course>` and source is read-only; inventory labels #08 `D` despite current route source; no Study Web route/runtime is present.
  - path: `.agents/worklog/2026-10-27/design-study-screen-sh06.md` (supplemental, historical)
    - carry_forward: Distinguish route-not-found from resource-not-found; never turn API 500/network errors into 404; use current screen-stitch assets and plan as authoritative over the older alternate handoff folder.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-06 only in this session. Recheck existing plan/DD/assets and current source; update `SH-06_PLAN.md` before any DD/marker/image edits; preserve `screen.png` and `code.html`; verify ordered one-to-one markers, A–F and event completeness; update the global tracker and worklog; distinguish DD, implementation and runtime status.
- Canonical contract/approved DD: Current `apps/study-client/docs/list_screen.md` SH-06 row and shared state/navigation rules; AC-05; API #08 catalog and current Study Server source/tests; linked SH-01/GS-01 contracts. Study Web design guide is visual target only. Study OpenAPI is `NOT_FOUND`.

## CURRENT_BEHAVIOR

- Source/config: Current SH-06 `screen.png`, `screen_annotated.png`, `code.html`, plan, DD and marker JSON exist. `apps/study-client/src/` and `apps/study-client/package.json` are absent; an ignored `dist/` directory exists but cannot establish editable router/runtime wiring. API #08 is registered under `/api/v1`, and the route delegates to its view. The view validates the path ID, selects only `PUBLISHED`, returns 404 `DESIGN_RESOURCE_NOT_FOUND` for invalid/missing/unpublished IDs, returns a singleton `Page<Course>` on 200, and returns safe 500 `DESIGN_INTERNAL_ERROR` for SQL/mapping errors. SQL errors roll back; no write/commit path is present.
- Runnable tests: `apps/study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py` contains source tests for invalid ID, missing row, DB error/rollback, success mapping and route success. Read only; tests were not run.
- Runtime wiring: Study Web UI/router is `UNWIRED`; API #08 route/module/test source exists locally, but deployed runtime and live database were not verified.

## SOURCE_TRACE

```text
Route GET /api/v1/courses/{course_id} in apps/study-server/app/api/v1.py -> get_course_detail -> validate_course_id/parse_integer -> FIND_PUBLISHED_COURSE_DETAIL via query_one (courses LEFT JOIN users, status=PUBLISHED) -> map_course + CoursePage(singleton) -> success_response/error_response; SQLAlchemyError rolls back and maps to safe 500. SH-06 UI caller/router is not traceable because Study Web src/package/router are absent. Test source covers invalid/missing/DB-error/success paths; it was not run.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #08 status labels | SH-06 row in `apps/study-client/docs/list_screen.md` says BE `D`; API index §5 row #008 says `R`; `docs/lists/list_api.md` labels the overall API contract `APPROVED_DESIGN_CONTRACT` and says not runtime-verified; API DD #08 overview says `Draft — Needs Confirmation`; current route/module/test source exists. | DISCREPANCY | Keep inventory, contract, API DD, source and deployment status distinct; do not infer runtime from source. |
| AC-05 not-found branch | AC-05 diagram says course not existing/not published → `404/403`; API contract lists 404/500; current #08 handler has no 403 branch, maps invalid/missing/unpublished to 404 and internal failures to 500. | BLOCKER / DISCREPANCY | Owner must resolve the contract/diagram meaning; preserve 403 as a separate external access-denied flow if a guard actually returns it. |
| Prototype surfaces | HTML has three hard-coded course cards/counts, contact link and footer links with `href="#"`; no IDs, API mapping, contact channel or destination contract is present. | BLOCKER | Product/UX must decide disposition and approved content/routes; do not treat mock data/links as runtime behavior. |
| Study Web integration | `apps/study-client/src/` and package manifest are absent; `dist/` exists. | IMPLEMENTATION BLOCKED | No source evidence for fallback route, CTA navigation, responsive behavior or service-error component. |
| Live DB/deployment | DDL and source are local artifacts; no live schema/deployment was checked. | NOT VERIFIED | Do not claim runtime behavior or live persistence. |

## CHANGES

- Files changed: `SH-06_PLAN.md` clarified API #08 status-label discrepancy and static counts; `SH-06.md` corrected API status/contract/source wording and references; `dd_screens/PLAN.md` updated the SH-06 blocker summary and F02 dependency note; this worklog records current source trace. Source image, HTML, annotated image and marker JSON were preserved.
- CONTEXT_UPDATES: none unless current source shows a canonical context page is materially stale.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router and preflight | Objective read; root router, `.agents/AGENTS.md`, context map and worklog contract/template reviewed. | VERIFIED |
| Docs worklog selector and review | `READY`, 3/255 exact-type logs; AD-01, AD-02 and AD-03 fully read; SH-06 logs from 2026-11-05/06 read; 2026-10-27 SH-06 history reviewed. | VERIFIED |
| Current source trace | API router prefix, route, view, validator, query, course models/helper, response helpers, DDL and focused test source read. Study Web source/package presence checked. No tests were run. | VERIFIED |
| Artifact/static verification | Both PNGs are 1600×1425; original `screen.png` hash `b6a423005ea008e9f00de6f2328f182c6256e7ae647575f55dfa8c4ae05ecf0a` and `code.html` hash `ce3c9bff0e9d24630172230f2b28e3a533ad4e2be1daecfe71f3bf1db4649ce7` match the plan. Marker JSON has 22 ordered IDs mapping 1:1 to 22 DD elements; all marker centers/targets are in bounds. Ten events are present. All 27 local DD links resolve; whitespace check passed. Visual review of annotated image completed. | VERIFIED |
| Repository checks | Final static audit passed: 22/22 marker-to-element map, 10 events, 27 DD local links, image/hash/bounds/whitespace checks; `git diff --check` passed for the tracked global plan. `node scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID` repository-wide because DB Admin context/source roots are absent and several scopes are stale; filtered output had no SH-06/worklog-specific diagnostics. This repo-level validator failure is recorded, not attributed to SH-06. | FAILED — REPO-WIDE CONTEXT |

## HANDOFF

- Remaining blockers: Product/UX decision on recommendation/contact/footer surfaces; AC-05 vs API #08 404/403 discrepancy; Study Web router/source missing; API status labels disagree; live DB/deployment unverified.
- Next owner/action: SH-06 static DD work is complete with the documented blockers; any repair of repository-wide context validation is separate. SH-07 is the next Screen ID in a separate session.
