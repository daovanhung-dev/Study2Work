---
task_id: "2026-11-07-design-study-screen-st13"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-12 → ST-13 student lesson flow; ST-13 inventory/AC/API contracts ↔ Study Server current source"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-13

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 240; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current behavior separation; source trace from client through auth/query/response/tests; retain static/mockup claims as non-runtime; do not claim tests, live schema or deployment verified.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer fields, enums, permissions or behavior from screenshot; source-backed test code does not establish live deployment; keep Study Web `UNWIRED` unless current editable source proves routing.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve identity/policy and API catalog/source discrepancies; trace errors and DB effect; keep API-DD Draft distinct from local source and screen DD status.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st12.md`
    - carry_forward: Recheck current lesson-to-quiz context and access/return boundaries; preserve live-schema and Study Web `UNWIRED` limits; keep no-test/no-runtime claims precise.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-13 only in this session; follow the supplied goal objective; inspect current inventory/contracts/source; create or update `ST-13_PLAN.md` before editing marker/DD artifacts; preserve original image/HTML; ensure ordered one-to-one markers and A–F DD with traceable events/APIs/states/navigation; update `list_screen.md`, global DD plan, and this worklog; distinguish DD readiness, implementation status and runtime verification.
- Canonical inventory row 27 proposes `/student/quizzes/:quizId`, AC-16, GET #28 and ST-14; ST-13 row says POST #29 after explicit Start. The same inventory's F05 and ST-14 row/DD conflict about #29 call-site/order. AC-16 precondition is Student entitlement plus open quiz; API #28/#29 catalogs are design contracts, and #28/#29 API DDs remain Draft. No owner decision resolves the screen handoff.

## CURRENT_BEHAVIOR

- `screen.png` 1349×1600 RGB; hash `b9cfdb6704a6d037a25803dfa271f96786b4ff0a708c4caaa30aac29320884f6`. `code.html` 8,568 bytes; hash `7640023e9147dfe7870528bbf9ade3024d3df374473ed2e8cdaa908de85d19d8`. PNG is a full quiz mockup; HTML is a different unavailable-state fallback with 15 static anchors and styling-only Tailwind CDN/config, without app request/form/control/event/timer code. Existing annotated PNG is 2698×3200; 30 markers/map/SVG were present before this turn.
- Study Web current tree has docs/assets and `tsconfig.tsbuildinfo`, no editable source, package manifest or router; serving/runtime is unverified (`UNWIRED`).
- Study Server `app/api/v1.py`, module tree and test tree contain no Student API #28/#29 route/module/test. Quiz routes #87–#91 are Admin APIs only. API catalog/DD do not prove runtime.
- AC-16 diagram sequence is GET #28 → eligibility decision → POST #29 → create `IN_PROGRESS`; AC-16 also describes 403/409 while #28 catalog has no 409. Attempt eligibility, deadline, attempt limit/resume, identity, response and retry/idempotency remain open in Q-28/Q-29.
- Legacy `infra/postgres/study-server/DB.sql` uses BIGINT `quizzes/quiz_attempts`; V1-PILOT `infra/postgres/02_study_db.sql` uses UUID `assessments/assessment_attempts`, with `quiz_questions.assessment_id` and `quiz_options`. Neither proves live schema; there is no approved mapping from API `quiz_id:int64` to the UUID model.
- Existing `ST-13.md` already has A–F, 30 element rows and EV-01…EV-05; static checks will verify exact mapping and links after edits.

## SOURCE_TRACE

```text
Expected: ST-13 screen inventory proposes GET #28 and explicit Start → POST #29 → ST-14; AC-16 requires authorized Student and open quiz. But F05 and the ST-14 inventory/DD disagree about #29 owner/order. API #28/#29 are design-only and no answer key may be exposed.
Current: Study Web has no editable Student source/router; API #28/#29 Student route/module/test are absent. Quiz route code is Admin #87–#91. Existing PNG/HTML differ; 30 marker artifacts are static. Legacy BIGINT and V1-PILOT UUID schema families differ. Existing ST-14 DD documents the #29 ownership/order conflict.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| PNG/HTML mismatch | Visual source PNG is a loaded overview; HTML is an unavailable fallback with static placeholder anchors. | `DISCREPANCY` | Preserve both; do not infer UI state/runtime from either alone. |
| Student APIs #28/#29 | Catalog/API DD exist; current router/module/test scan found no Student implementation; #87–#91 are Admin quiz APIs. | `NOT_FOUND / DECLARED_NOT_RUNNABLE` | Screen data/create-attempt flow cannot be runtime verified. |
| #29 screen owner/order | ST-13 row says POST after Start; F05 and ST-14 row place it differently; ST-14 DD records the conflict. ST-14 path requires `attemptId` before entry. | `DISCREPANCY / OWNER DECISION REQUIRED` | Do not call POST twice or finalize handoff/entry route. |
| Quiz persistence model | Legacy DDL is BIGINT `quizzes/quiz_attempts`; V1-PILOT uses UUID Assessments/AssessmentAttempts. | `DISCREPANCY / LIVE SCHEMA NOT VERIFIED` | Do not infer API-to-schema mapping or write behavior. |
| Study Web wiring | No editable source/package/router; context status `UNWIRED`. | `UNWIRED` | No implementation/runtime claim. |

## CHANGES

- Files changed: this worklog; `ST-13_PLAN.md`; `ST-13.md`; ST-13 row and F05 handoff note in `apps/study-client/docs/list_screen.md`; ST-13 row/checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Preserved `screen.png`, `code.html`, `screen_annotated.png`, marker JSON and SVG after static/visual review; no marker regeneration was needed.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; API owner decisions and schema mapping remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective reread; root/global routers, context map, worklog README/template, web-work/Study Web and server-study scope contexts, cross-scope project pages and skill registry read; exact docs selector READY 3/240; AD-01/02/03 worklogs and direct upstream ST-12 worklog read. Registry excludes UI-only DD from canonical skills. | VERIFIED |
| Contract/source trace | Inventory/F05, AC-16 index and diagram, API catalog #28/#29, API DD/open questions, ST-14 DD, current Study route/module/test source, Study Web tree and both schema artifacts reviewed. No application tests run. | VERIFIED |
| `file .../{screen.png,screen_annotated.png}` + inline Python static audit | Original hashes match plan; dimensions are 1349×1600 / 2698×3200; direct visual review; marker JSON/SVG valid, 30 sequential unique in-bounds labels and 30 DD rows exact 1:1; HTML/links/local paths checked. | VERIFIED |
| Optional Pillow metadata check | Python Pillow import unavailable; image dimensions were checked with `file`. | DECLARED_NOT_RUNNABLE; alternative evidence used |
| Plan-before-DD gate | Added dated source/asset re-audit to `ST-13_PLAN.md` before editing DD or trackers; no marker/image rewrite was required. | VERIFIED |
| `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` + inline link/whitespace check | Relative Markdown paths resolve in ST-13 DD/plan, worklog and both trackers. Authored ST-13/worklog/global-plan files have no trailing whitespace; `list_screen.md` lines 3–6 contain baseline whitespace identical to HEAD and outside our changed hunks. Scoped diff check exits 0; ST-13 row, F05 and global checkpoint carry the blockers/statuses. | VERIFIED |

| Application tests/runtime/live DB | Not run; no implementation or live-schema verification was requested or claimed. | NOT_RUN |

## HANDOFF

- Remaining blockers: quiz eligibility/open/deadline and answer exposure; attempt limit/resume/idempotency and #29 response; single #29 screen owner/order; BIGINT legacy vs UUID V1-PILOT schema mapping and live DB; PNG/HTML discrepancy; Study Web route/runtime and CTA destinations.
- Next owner/action: complete ST-13 only; do not start another Screen ID in this session.
