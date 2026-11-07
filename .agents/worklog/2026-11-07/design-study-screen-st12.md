---
task_id: "2026-11-07-design-study-screen-st12"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-11 → ST-12 lessonId/position/resource-panel return context; API #26 resources → API #12 detail; AC-15; Study Web source/runtime boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-12

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 239; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; trace source and API status; preserve Study Web `UNWIRED`; do not infer UI/API mappings or runtime from mockups/tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: UI-only DD has no canonical skill; keep API catalog separate from local source; trace auth, query, DB effect, response and focused tests without running tests unless requested.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer identity, privacy, audit or behavior from mockups; preserve local-source/API-DD differences and live-schema limitations.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st11.md`
    - carry_forward: ST-11 marker/DD audit is complete; ST-11 and ST-10 both mention #24; ST-09 lessonId handoff, #26 Resource response/security, and ST-12 return-to-player context remain unresolved. Recheck current sources this session.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-12 only in this session. Inspect the inventory, AC-15, APIs #26/#12, current server/client sources and existing assets; write `ST-12_PLAN.md` before marker/DD edits; preserve original assets; ensure ordered one-to-one markers and an A–F DD; update only ST-12 tracker rows and this worklog; keep unresolved response, authorization, URL and return-context decisions explicit.
- Canonical details: Inventory ST-12 row 26 proposes `/student/lessons/:lessonId/resources`, AC-15, #26 and #12; #12 is called only if a valid `resource_id` exists. API #26 catalog/AC declare Student Bearer and `ApiEnvelope<Lesson>`, leaving the Resource collection shape unresolved. Do not infer cardinality, URL signing, automatic download/open, playback-position persistence, or return semantics.

## CURRENT_BEHAVIOR

- Source/config: Current ST-12 asset is a static unavailable/resource-policy fallback. HTML has 14 `href="#"` anchors with `data-path`, no API call/listener/timer/player/form. Study Web has no editable app source/package/router; ignored dist has no ST-12 route. API #26 has no Student route/module/query/test. API #12 has current route/module/query/model and focused test source; it returns direct stored URL with no auth, visibility/enrollment check or signer. Its DD cover claim that runtime/OpenAPI is not verified is stale against current route/test source; API DD remains Draft.
- Data design: Legacy BIGINT candidate `DB.sql` has nullable `resources.lesson_id` and no visibility; scoped V1-PILOT DDL has no `resources` table declaration. Neither proves live schema or an approved visibility/access mapping.
- Runnable tests: API #12 focused test source read only; no application tests were run.
- Runtime wiring: Study Web remains `UNWIRED`; API #26 is `NOT_FOUND`; API #12 is source-backed locally. No browser/runtime or deployment evidence.

## SOURCE_TRACE

```text
Expected: Inventory/AC-15 proposes ST-11 lesson context → #26 attached resources → optional #12 for a valid selected `resource_id` → a policy-approved resource viewer/handoff and return. The catalog's #26 response is Lesson, so the expected resource list contract is unresolved. AC-06 signer flow is a separate design source that conflicts with #12 current behavior.
Current: ST-12 HTML is a static fallback, all anchors are placeholders and no resource item exists. #26 route/module/query/test is absent. #12 route source registers `GET /api/v1/resources/{resource_id}`; its view validates positive signed-int64, reads resource, conditionally checks a non-DELETED lesson and PUBLISHED course when `lesson_id != null`, returns `id/name/type/url/lesson_id` with stored `url`, skips visibility/enrollment/auth/signer, maps invalid/missing/parent denial to 404 and SQL/mapping failure to 500; SQLAlchemy failure rolls back. Focused test source characterizes fake-DB behavior/OpenAPI; tests were not run. Live DB/runtime are unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #26 contract/current implementation | Catalog and AC-15 say Student Bearer and `ApiEnvelope<Lesson>`; no Student route/module/query/test. Q-26-01…07 stay open. | DISCREPANCY / NOT_FOUND | Cannot create Resource list, item or resource ID from the current contract. |
| API #12 expected/current behavior | Catalog public `Resource`; AC-06 includes access and a private-resource signer; current source is public and returns stored URL with no visibility/enrollment/signer. | DISCREPANCY / SOURCE_BACKED LOCALLY | Block safe expose/open/download pending owner-approved access and URL policy. |
| API #12 DD currentness | Cover says no runtime/OpenAPI verification, while route and focused test source exist in current tree. | STALE DD / SOURCE-DOCUMENT DISCREPANCY | Retain Draft approval state; screen DD identifies the source discrepancy without editing API DD. |
| Asset and resource selection | Prototype is static, contains no Resource item or click target; all 14 anchors are placeholders. | CURRENT STATIC / UNWIRED | Cannot call #12 or preserve resource-selection/return context in current UI. |
| Database/schema | Legacy BIGINT DDL has `resources.lesson_id` nullable/no visibility; scoped V1-PILOT DDL has no `resources` table; live schema unknown. | BLOCKER | Do not conflate schema models or infer visibility/authorization. |

## CHANGES

- Files changed: this worklog; `ST-12_PLAN.md` (dated re-audit and verified checklist/results); `ST-12.md` (source/DD discrepancy and schema blocker); ST-12 row in `list_screen.md`; ST-12 row and checkpoint in `dd_screens/PLAN.md`.
- Marker JSON/SVG, source images and annotated PNG were audited and kept unchanged.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; #26/#12 owner decisions remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog preflight | Objective and context/worklog instructions reviewed; exact docs selector `READY` 3/239; AD-01, AD-02, AD-03 fully read; direct upstream ST-11 worklog reviewed. | VERIFIED |
| Scoped source and contract review | ST-12 inventory/AC-15, API catalog #12/#26, #26 open questions, #12 current route/module/query/model/test source and API DD cover/data mapping, Study Web tree, ST-11/GS-07, legacy/V1-PILOT DDL reviewed read-only. | VERIFIED |
| Plan-before-DD gate | Existing plan re-audited and dated before DD edits; planned DD/tracker changes documented. | VERIFIED |
| Static artifact audit | JSON/SVG XML parse; 27 IDs and labels match 27 DD rows; embedded image equals source bytes; source hashes preserved; local Markdown links resolve; HTML/PNG/marker geometry reviewed. | VERIFIED |
| DD/tracker audit | A–F headings and EV-01…EV-05 present; inventory/folders 83/83, core bundles 82/83 (ST-01 missing); ST-12 tracker statuses updated. | VERIFIED |
| Whitespace and diff check | Authored ST-12/worklog text has no trailing whitespace; scoped `git diff --check` for tracked tracker files passed. | VERIFIED |
| Tests/runtime | No application tests/browser runtime/deployment/live DB check was run. | NOT RUN (per task scope) |

## HANDOFF

- Remaining blockers: #26 resource payload/cardinality/access/empty rules; #12 direct public URL/access risk and stale API DD cover; resource selector/item and `resource_id` handoff; ST-11 return context; schema/live DB alignment; Study Web route/runtime.
- Next owner/action: ST-12 session complete; stop here. ST-13 is next in a separate session.
