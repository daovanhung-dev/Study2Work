---
task_id: "2026-11-07-design-study-screen-st14"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-13 → ST-14; Study API #28–#30 / AC-16; downstream ST-15 #31 and ST-16 #32"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-14

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 241; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current source separate; preserve original screen assets; compare API catalog/DD with server routes/tests and Study Web wiring; do not infer behavior from static UI; distinguish DD, implementation and runtime status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: A cataloged API may have local source while its DD remains Draft; document prototype behavior and server behavior separately; do not treat fake DB tests as deployed/live-schema evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Carry fields only from approved contract/current source; preserve policy gaps; keep Study Web `UNWIRED` absent editable source/router.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st13.md`
    - carry_forward: ST-13 sets GET #28 before explicit Start → POST #29; current inventory/F05 discrepancy and ST-14 path requiring `attemptId` leave a single #29 owner/handoff decision open. Keep legacy BIGINT and V1-PILOT UUID schema families separate; neither is live schema evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-14 only in this session under the supplied goal objective. Audit current screen/design/API/DB/source evidence; update plan before DD or tracker edits; retain source assets; preserve ordered unique one-to-one marker mapping; maintain A–F, element/event/state/navigation/source trace; update the ST-14 inventory row, F05 handoff summary and global plan; distinguish `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED`.
- Canonical contract/approved DD: AC-16 order is GET #28 → read Quiz/rules/question set → eligibility → POST #29 creating `IN_PROGRESS` Attempt → answer via PUT #30 → #31 submit → #32 result. API catalog/DD and DB sources must remain distinct from runtime behavior.

## CURRENT_BEHAVIOR

- **Study Web:** current `apps/study-client/` has `docs/`, ignored `dist/`, `node_modules/` and `tsconfig.tsbuildinfo`; no editable `src/`, package manifest, router or Student screen. Current Study Web status is `UNWIRED`; serving/runtime is unverified.
- **Study API:** current `app/api/v1.py` route scan and Student module/test path scan found no Student APIs #28–#32. Quiz routes #87–#91 are Admin-only. Catalog and API DDs #28/#29/#30 are design-only; all three DDs are `Draft — Needs Confirmation`. API #28/#29/#30 open questions remain unresolved. No current answer-write or attempt-read/restore source exists.
- **Assets:** `screen.png` is 1600×1468 RGB, SHA-256 `63ab0e25bd3c502d5f2ce699e93df046532a32862aa0256d3bb5bca1cae89cb8`; `code.html` is 6,636 bytes, SHA-256 `0579187c7347daaf9e48118f4422fef7dc719f00345f01b6f2fe1a15669afdfc`; both match the plan and remain unchanged. HTML is an unavailable-state fallback with two static anchors and no form/input/native button/event handler/API/timer logic. PNG is a loaded quiz mockup, so the assets show different UI states.
- **API/flow discrepancy:** AC-16 order is GET #28 then eligibility then POST #29. ST-13 row/DD assigns #29 to Start; ST-14 inventory also listed #29 though its route already required `attemptId`. The screen owner and entry handoff are unresolved; do not POST twice.
- **API #30:** catalog body retains `question_id:int64!` and ambiguous `answer(s):string!`; request JSON property/representation, validation, persistence/upsert key, transaction/concurrency, ownership/status, answer projection/disclosure and retry semantics are open. Catalog #30 does not declare 409. Inventory has no GET attempt/answers for refresh/resume.
- **Database artifacts:** legacy `DB.sql` uses BIGSERIAL/BIGINT quiz/attempt/answer IDs, one `quiz_answers.choice_id` per row and no unique `(attempt_id, question_id)` pair. V1-PILOT `02_study_db.sql` uses UUID assessments/attempts/answers; attempt requires `submitted_payload_snapshot` and defaults to `SUBMITTED`, while answer payload is declared immutable after submit. No approved mapping to API int64 or pre-submit autosave exists; live schema is unverified.
- **Visual sample uncertainty:** two timers; `14/20` progress while answered/unanswered counters are `13/6`; the flagged count's overlap rule is unknown. No time source, progress formula, flag persistence, realtime or idempotency guarantee is established by the screenshot.

## SOURCE_TRACE

```text
Expected: AC-16 GET #28 → Quiz/rules/questions → eligibility → POST #29/IN_PROGRESS → Student answers → PUT #30 UPSERT → ST-15 #31 → ST-16 #32.
Current: Study Web has no editable route/client source → Study Server has no Student #28–#32 route/module/test → no current answer write, attempt restore, response mapping or runtime caller exists. Admin #87–#91 are separate. Legacy/V1-PILOT DDL artifacts are incompatible design candidates, not live schema evidence.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #29 call-site and entry | AC-16 requires #28 → eligibility → #29; ST-13 associates #29 with Start, while ST-14 also lists it and requires `attemptId` on its path. | `DISCREPANCY / BLOCKER` | Product/API owner must decide one trigger and route handoff; do not double-create an attempt. |
| #30 request and write contract | Catalog `answer(s):string`; Draft DD Q-30-01..06 leave JSON shape, storage, upsert, concurrency, ownership/state, response and retries open. | `BLOCKER / DRAFT` | Cannot specify executable autosave or safe retry without guessing. |
| Resume and timer | No GET attempt/answer API in inventory; no authoritative timer source/deadline; counters have no formula/overlap rule. | `BLOCKER / SOURCE_REQUIRED` | Refresh, direct entry, answer restore, expiry and timer states cannot be finalized. |
| DDL/schema | Legacy BIGINT `quiz_*` tables differ from V1-PILOT UUID assessment tables and immutable submitted answer lifecycle. | `DISCREPANCY / LIVE SCHEMA NOT VERIFIED` | No approved API-to-storage mapping; neither DDL artifact proves live state. |
| Current wiring | Study Web source/router absent; Student #28–#32 route/module/test absent; #87–#91 are Admin quiz routes. | `UNWIRED / NOT_FOUND / DECLARED_NOT_RUNNABLE` | No implementation, endpoint or runtime claim. |
| Mockup vs HTML | PNG is a loaded quiz; HTML is a static unavailable fallback with two anchors and no handlers. | `DISCREPANCY` | Keep both source assets and do not infer runtime from them. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_PLAN.md`, `ST-14.md`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog.
- `ST-14_PLAN.md`: re-audit recorded before DD/tracker edits; added V1-PILOT DDL link and exact AC-16 order/schema evidence.
- `ST-14.md`: tightened #29 ownership/order, recorded V1-PILOT submitted-snapshot/immutability mismatch, clarified screenshot counter ambiguity and marked completed static audit. Retained `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.
- `list_screen.md`: ST-14 row now follows AC-16 API order and records unresolved screen owner/handoff; F05 distinguishes #29/#31 409 from #30's catalog without 409.
- `dd_screens/PLAN.md`: updated ST-14 blocker row and appended dated checkpoint.
- Original `screen.png` and `code.html`, marker JSON/SVG and annotated PNG were preserved. No other Screen ID, API contract/source or context page changed.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none; open owner decisions remain blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Read the objective file; root/global router, context map, worklog README/template; exact-type selector `READY` 3/241; read AD-01, AD-02, AD-03 and direct ST-13 dependency worklog. Registry confirms Web UI-only DD has no canonical skill. | VERIFIED |
| Scope/context and source review | Read project architecture/dependency/contracts/database/status context; Web Work + Study Web entry/index/design target; Study Server entry/index/routes/database/tests/workflows; inventory/F05, AC-16 index/diagram, API #28–#30 catalog/DD/open questions, current router/module/test scans and both DDL families. | VERIFIED |
| Plan-before-DD gate | Added the dated re-audit to `ST-14_PLAN.md` before modifying `ST-14.md` or shared trackers. | VERIFIED |
| Asset/marker static audit | `screen.png` 1600×1468; annotation 3200×2936 (2×); source hashes match plan. JSON has 32 ordered unique/in-bounds markers; SVG has 32 groups with coordinates/labels matching JSON; DD has 32 exact element rows; 10 event IDs and A–F sections present. Images reviewed visually. | VERIFIED |
| HTML static audit | Parser found 2 static anchors, 0 forms/inputs/native buttons/inline event attributes, no fetch/XHR/WebSocket/timer call strings. | VERIFIED |
| Links/inventory | All relative links in ST-14 plan/DD resolve; inventory has 83 unique IDs matching 83 folders; 82/83 have the six core artifacts, with ST-01 still incomplete. | VERIFIED |
| `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` | Exited 0 with no whitespace errors in changed hunks. | VERIFIED |
| Context validation | `node scripts/validate-agent-context.mjs` exits 1 with `AGENT_CONTEXT_INVALID`: missing `.agents/db-admin/*` pages and `apps/db-admin-*` source roots, plus `CONTEXT_STALE` across server-study/server-work/web-work/mobile-work/db-admin. A filtered rerun found no diagnostics referencing ST-14, `list_screen.md`, the screen tracker or this worklog. These are existing repository/context drift outside this task's files. | PRE-EXISTING CONTEXT INVALID |
| Application tests/browser runtime/live DB | Not run; not claimed. | NOT_RUN |

## HANDOFF

- Remaining blockers: owner decision for #29 trigger and route handoff; #30 answer property/storage/upsert/access/state/response/retry contract; restore/resume endpoint; authoritative time/progress/flag rules; approved schema mapping and live DB status; Study Web Student routes/API implementation.
- Session outcome: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Documentation and static audit are complete for ST-14; no application tests or runtime run.
- Next owner/action: ST-15 in a separate session, after ST-14 is finished. Do not start another Screen ID in this session.
