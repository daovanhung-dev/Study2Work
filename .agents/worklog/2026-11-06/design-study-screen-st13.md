---
task_id: "2026-11-06-design-study-screen-st13"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-13 → ST-14; API #28 quiz detail → API #29 attempt creation; AC-16; G-09"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-13

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 174 exact-type `docs` worklogs; no shortage.
- prior_worklogs_reviewed:
  - `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve originals/hashes; keep expected contract separate from current source; Study Web is UNWIRED; do not infer route/cache behavior from a static prototype.
  - `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep screenshot/HTML actor/state discrepancies explicit; trace APIs against current source; do not treat catalog-only APIs as runnable.
  - `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; source-backed API does not prove UI/runtime wiring; preserve API and source discrepancies.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Re-read objective: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`. This session handles ST-13 only and requires plan-first, source-traced DD, annotation, tracker/worklog and static audit.
- Inventory row 27: Student route design `/student/quizzes/:quizId`, AC-16, API #28, ST-14 next, states loading/closed/available/denied. Expected GET #28 for permitted metadata/questions; POST #29 only after explicit Start.
- API catalog #28: Student Bearer, GET `/api/v1/quizzes/{quiz_id}`, path `quiz_id:int64!`, `ApiEnvelope<Quiz>`, 200/401/403/404/500.
- API catalog #29: Student Bearer, POST `/api/v1/quizzes/{quiz_id}/attempts`, path only/no body or query, `ApiEnvelope<QuizAttempt>`, 201/401/403/404/422/409/500.
- AC-16 precondition requires entitled Student and open quiz. AC diagram reads quiz/rules/questions, evaluates eligibility, then creates an IN_PROGRESS attempt. G-09 and API #28/#29 DDs leave answer exposure, duration, eligibility, attempt limit/expiry, conflict and response details open.
- Do not turn mockup sample values, proctoring, timer, auto-save, grading or certificate copy into business rules.

## CURRENT_BEHAVIOR

- ST-13 folder initially contained only `screen.png` and `code.html`. PNG is 1349×1600 RGB, SHA-256 `b9cfdb6704a6d037a25803dfa271f96786b4ff0a708c4caaa30aac29320884f6`. HTML is 8,568 bytes, SHA-256 `7640023e9147dfe7870528bbf9ade3024d3df374473ed2e8cdaa908de85d19d8`.
- PNG is a full quiz overview with sample metrics/history and proctoring/auto-submit/certificate claims. HTML is a static unavailable-information fallback with a return-to-courses link; no fetch, timer, state handler or router handler. Preserve both originals.
- API #28/#29 are catalog and Draft DD only. Current Student route/module/test scan found no #28/#29 implementation; current Admin quiz APIs #87–#91 are different routes. Candidate `DB.sql` is checked-in design evidence, not live-schema verification.
- Study Web context is UNWIRED: editable Student source/router/package absent; do not infer browser behavior from HTML or ignored dist.
- AC-16 diagram names five API calls and an eligibility branch. API #28 catalog lacks 409 even though the diagram associates a 403/409 branch with expired/exhausted attempts. Keep this discrepancy.

## SOURCE_TRACE

- Screen inventory/F05/G-09: `apps/study-client/docs/list_screen.md`.
- UI assets: `apps/study-client/docs/screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/screen.png` and `code.html`.
- API contracts: `docs/lists/list_api.md`; #28/#29 API DD and OPEN_QUESTIONS.
- AC: `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` and `AC_02_STUDENT_LEARNING.drawio`.
- Current backend: `apps/study-server/app/api/v1.py`, app/modules, tests and `.agents/server-study/apis/declared-routes.md`. Search found only Admin quiz routes #87–#91, no Student #28/#29. No current callers/callees or API #28/#29 DB effects exist to trace.
- Candidate data: `infra/postgres/study-server/DB.sql` contains quizzes, quiz_questions, quiz_choices, quiz_attempts and quiz_answers; foreign keys/status/duration are not live schema evidence. API #29 design intends attempt creation; runtime mutation/transaction is absent.
- Study Web design guide is intended-only; no UI runtime source or tests were executed.
- API #28 DD excludes is_correct from Student projection. API #29 DD leaves eligibility owner, identity, limit/expiry/resume, idempotency and initial response details open.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| PNG versus HTML | Full quiz overview versus static unavailable fallback. | `DISCREPANCY` | Cannot treat either as runtime state. |
| API #28/#29 current implementation | Catalog/API DD exist; current Student route/module/test absent. | `NOT_FOUND` / `DECLARED_NOT_RUNNABLE` | Screen data and Start cannot be runtime verified. |
| Study Web | No editable source/router; static anchors only. | `UNWIRED` | Auth, fetch, CTA and navigation behavior absent. |
| Sample quiz metrics/history | Not in logical Quiz response; no ST-13 history API source. | `DESIGN_ONLY` | No invented default or API mapping. |
| Timing/answer/security/grade claims | G-09 and API DD questions open; no timer/webhook/proctoring source. | `SOURCE_REQUIRED` | Do not expose answers or claim enforcement. |
| Eligibility/attempt lifecycle | AC-16 vs catalog error mapping; #28/#29 open questions. | `BLOCKER` | Available/closed, retry/resume and 403/409 remain unresolved. |
| Database | Checked-in DDL only; no live schema evidence. | `NOT_VERIFIED` | No runtime persistence claims. |

## CHANGES

- Created `ST-13_PLAN.md` before marker/DD work.
- Created 30-element `ST-13_markers.json` and transparent `ST-13_markers_overlay.svg`; rendered `screen_annotated.png` from source PNG at 2×. Reviewed image and moved markers away from text/control labels.
- Created `ST-13.md` with A–F, 30 mapped elements, 5 events, API request/response/error mapping, state/navigation, security, discrepancies, blockers and source links.
- Updated `dd_screens/PLAN.md`: ST-13 blocker/status, 22/83 complete bundles, 61 incomplete, implementation/runtime status and next pointer ST-14.
- Context pages/manifest: unchanged. No API catalog, backend, database or runtime behavior changed.
- No tests, browser flow or runtime calls executed.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Objective and preflight | Re-read goal objective; exact-type docs selector selected 3 worklogs and the three selected files were reviewed. | VERIFIED |
| Current source/contracts | Inventory/F05/G-09, PNG/HTML, API #28/#29 catalog and DD/open questions, AC-16 index/diagram, Study router/module/test search, candidate DB DDL and Study Web context/design read. | VERIFIED (static source trace only) |
| Original assets | PNG SHA-256 b9cfdb6704a6d037a25803dfa271f96786b4ff0a708c4caaa30aac29320884f6 and HTML SHA-256 7640023e9147dfe7870528bbf9ade3024d3df374473ed2e8cdaa908de85d19d8 match recorded baseline; source PNG 1349×1600. | VERIFIED |
| Annotation | 30 sequential unique markers are within source bounds and map one-to-one to 30 DD element IDs; overlay has 30 labels; annotated PNG is 2698×3200 (2×); visual review completed. | VERIFIED |
| Local references | All relative Markdown links in ST-13_PLAN.md and ST-13.md resolve. | VERIFIED |
| Global inventory/tracker | 83 inventory IDs; 22 complete artifact bundles and 61 incomplete; ST-13 row is BLOCKED on DD/implementation/runtime axes; next pointer ST-14. | VERIFIED |
| Whitespace | git diff --check is clean; added ST-13 Markdown/JSON/SVG files have no trailing whitespace. | VERIFIED |
| Context validator | Not run: no agent context page or manifest was changed; only worklog, per-screen DD/assets and the tracker changed. | NOT_REQUIRED |
| Tests/browser/runtime | Not run; this session documents static design/source and performs static artifact checks only. | NOT_RUN |

## HANDOFF

ST-13 remains `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`. Next screen for a separate session: ST-14.

