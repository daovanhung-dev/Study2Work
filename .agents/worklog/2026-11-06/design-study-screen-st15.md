---
task_id: "2026-11-06-design-study-screen-st15"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-14 → ST-15 pending answer flush; API #30 → #31 submit; AC-16; G-09; ST-16 result handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-15

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs selected of 176 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve original assets and separate expected/current behavior; Study Web remains UNWIRED; HTML, catalog and static mockup do not prove runtime navigation/API behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace current backend separately from API declaration; keep response/source discrepancies explicit; tests and checked-in DDL do not prove live runtime/schema.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: A UI-only DD has no wired canonical skill; preserve source/contract mismatch and linked-screen handoff decisions instead of inferring them.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Re-read the goal objective before continuing. This session handles ST-15 only; write the per-screen plan before marker/DD work; preserve original assets; create a marker map, annotated image and DD; update the 83-screen tracker and this worklog; keep DD/implementation/runtime statuses distinct.
- Inventory: Student confirmation dialog at `/student/attempts/:attemptId/submit`, AC-16, APIs #30/#31; show unanswered count, confirm, lock editing when server accepts; flush pending #30 then POST #31 once, then ST-16; handle double-submit/409. States: `confirm/submitting/submitted/ambiguous-network`; links ST-16 and ST-14.
- F05 sequence: ST-13 #28 → Start → ST-14 #29 → #30 save answer → ST-15 #31 submit after pending flush → ST-16 #32 result. G-09 blocks answer versioning/autosave, submit idempotency and deadline/time policy; do not expose correct answers before policy allows.
- API #31 catalog: Student Bearer; POST `/api/v1/attempts/{attempt_id}/submit`; required `attempt_id:int64!`; no query/body; `ApiEnvelope<QuizAttempt>`; 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/409/500 with catalog codes.
- AC-16: Student must be eligible and quiz open; #31 sets candidate attempt to `SUBMITTED`, performs automatic grading, then `PENDING_GRADE` if manual grading remains or `GRADED` otherwise; #32 reads permitted result. Grading formula, manual-question detection, repeat-submit policy, status enum and disclosure remain open.
- API #31 DD is `Draft — Needs Confirmation`; ownership/masking, allowed state/expiry, duplicate/concurrent submit, grading transaction/rollback, score/timestamp and response projection remain unresolved. API #30 DD leaves answer shape, flush/retry/idempotency/versioning, persistence and outcome reconciliation unresolved.

## CURRENT_BEHAVIOR

- `screen.png` is 1600×1280 RGB, SHA-256 `40d47787f58e9f962237ef41f4fbc58f8d2600d38f51f061cdffefb8a6d4aedc`. It shows the fixed header plus dimmed/blurred quiz and a submit-confirmation modal with 18/20 answered, two unanswered (Q19/Q20), one flagged (Q15), 12:15 remaining, “synced 18/20,” policy/attempt text, Continue and Submit Now controls.
- `code.html` is 12,313 bytes, SHA-256 `6debc6c68e6d046106e377876f34bb68ed3682480118903989ed32318f0d7976`. It shows a different fallback: blurred question 18/20 background, a message that valid work is not recorded and cannot be submitted, and only a “Quay lại kiểm tra” button. No visible submit button, API request or request body exists.
- Static HTML script queries `btn-submit-exam`, which is absent; that dormant branch would disable the button and after 600 ms navigate to hardcoded `#/student/attempts/att-react-02/result`. `btn-cancel-dialog` exists and calls `window.history.back()`. This is prototype JavaScript, not a Study Web route or server call.
- Screenshot claims instant Cloud LMS grading/skill chart, attempt 2/3 with one attempt remaining, and time/sync counts. These have no source in the #31 response/AC beyond PENDING_GRADE vs GRADED branches; the 12:15 and header 45:20 timers disagree. ST-14 is a different snapshot (14/20 with 13 answered + 6 unanswered + 1 flagged); no confirmed state-transfer source ties the samples together.
- Study Web has docs/assets and ignored compiled `dist` with only a root route; no editable app source/package/router or Student screen implementation is present; serving is unverified (`UNWIRED`).
- Current Study Server scan found no Student API #31 route/module/test or submit caller. Admin quiz APIs #87–#91 are separate. Therefore no current #31 DB write, lock, grading, response or runtime side effect exists to trace.
- API #31 DD is design-only. Candidate `quiz_attempts` update and `quiz_answers` grading are not live DB evidence; checked-in DDL has nullable submitted_at/score, `status` default `IN_PROGRESS` without canonical enum and `quiz_answers.is_correct NOT NULL`; exact transaction and state/grade values remain open.

## SOURCE_TRACE

- `apps/study-client/docs/list_screen.md`: ST-15 row, F05 and G-09; confirm/flush/submit/result order and linked screens.
- `apps/study-client/docs/screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/{screen.png,code.html}`: unchanged source asset and companion fallback; static DOM/JS control IDs inspected.
- `apps/study-client/docs/screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14.md`: predecessor submit handoff says ST-15 receives `attemptId`, flushes pending #30 and invokes #31 only after confirmation; direct resume/data transfer is unresolved.
- `docs/lists/list_api.md` rows #30–#32 and `QuizAttempt`/`QuizAnswer` schemas; API #31 DD files `00_Cover.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`; API #30 open questions.
- AC evidence: `.agents/server-study` route/architecture pages, `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-16 and `AC_02_STUDENT_LEARNING.drawio` submit/grading branch.
- Candidate DB evidence: `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` and `infra/postgres/study-server/DB.sql`; no live-schema claim.
- Current wiring evidence: `apps/study-server/app/api/v1.py`, `app/modules/`, `tests/`, `.agents/server-study/apis/declared-routes.md`; no Student #31 route/module/test found. `.agents/web-work/study/AGENTS.md` and `INDEX.md` confirm no editable Study Web source.
- Intended UI target: `.agents/web-study/design.md` calls for ≥44px controls, visible focus states, keyboard operation, reduced-motion handling and no color-only state. These are target requirements, not runtime evidence.
- Registry: `.agents/context-manifest.json` and `.agents/skills/INDEX.md` exclude `web-ui-only-dd` from canonical skills; no UI-only skill applies.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST15-D01 | PNG confirmation modal and HTML unavailable/error fallback do not show the same state; HTML submit handler target is absent. | `DISCREPANCY` | Document both separately; neither proves runtime. |
| ST15-D02 | UI shows counts, synced answers, remaining time, attempt 2/3 and instant grading/skill chart; response/AC/schema do not supply or confirm these values/policies. | `DESIGN_ONLY / SOURCE_REQUIRED` | Do not bind sample values or claim immediate grading. |
| ST15-D03 | Inventory requires pending #30 flush before #31; #30 payload/upsert/order/retry/idempotency/outcome are unresolved in G-09 and API #30 Qs. | `BLOCKER — dependent contract` | Cannot define a safe flush barrier/retry or exact summary counts. |
| ST15-D04 | API #31 DD Q-31-01..06 leaves ownership/state/expiry/duplicate/concurrency/grading/transaction/response/timestamp/error predicate open. | `BLOCKER — API/DB contract` | Cannot finalize submit/recovery/result behavior. |
| ST15-D05 | Current Study Web has no editable routes; Study Server has no Student API #31 route/module/test. | `UNWIRED / NOT_FOUND / DECLARED_NOT_RUNNABLE` | No UI handler, API submit or DB mutation is runtime-verified. |
| ST15-D06 | HTML fallback’s visible text blocks submit, while its dormant missing-button handler would hardcode a result hash after 600 ms. | `DISCREPANCY / STATIC PROTOTYPE` | Do not use the JS branch as route/API contract. |

## CHANGES

- Files created: `apps/study-client/docs/screen_stitch/03_student/ST-15_xac-nhan-nop-bai-kiem-tra/ST-15_PLAN.md`, `ST-15.md`, `ST-15_markers.json`, `ST-15_markers_overlay.svg`, and `screen_annotated.png`.
- Updated `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`: ST-15 is DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED; complete artifact set count is 24/83; next pointer is ST-16.
- Preserved source `screen.png` and `code.html`; both hashes match the initial baseline. No context pages changed.
- No tests or runtime operations were run. No canonical UI-only DD skill is wired for this screen.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Goal/context/worklog preflight | Goal objective, router/context map/worklog contract read; selector returned three exact-type docs worklogs and all three were read. | VERIFIED |
| Source asset integrity | `screen.png` SHA-256 `40d47787f58e9f962237ef41f4fbc58f8d2600d38f51f061cdffefb8a6d4aedc`, 1600×1280; `code.html` SHA-256 `6debc6c68e6d046106e377876f34bb68ed3682480118903989ed32318f0d7976`, 12,313 bytes. | PASS |
| Marker/DD map | Read-only Python static audit: 18 markers in numeric order, all within source bounds, one corresponding DD element row each; annotated PNG is 3200×2560; overlay SVG parses and has 18 circles and 18 labels. | PASS |
| Relative links | Read-only Python audit over local Markdown links in ST-15 plan and DD; all resolve. | PASS |
| Inventory/tracker | Read-only Python audit: 83 unique inventory IDs match 83 screen folders; 24/83 full artifact sets including ST-15; tracker row/status/count and ST-16 pointer agree. | PASS |
| Whitespace | `git diff --check` | PASS; no output |
| Tests/runtime | Not run; user goal requires static verification only unless tests are requested. No runtime verification claimed. | NOT RUN |

## HANDOFF

- Remaining blockers: API #30 flush shape/order/idempotency/reconciliation; API #31 ownership/state/repeat/expiry/grading/transaction/response; ST-14 handoff/summary and timer policy; PNG/HTML discrepancy; Study Web remains UNWIRED and Student #31 NOT_FOUND.
- Next owner/action: ST-16 is the next session; do not process another Screen ID in this session.
