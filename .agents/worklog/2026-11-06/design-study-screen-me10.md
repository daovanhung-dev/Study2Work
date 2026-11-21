---
task_id: "2026-11-06-design-study-screen-me10"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-10 consumes API #55 submission detail, then calls #56 grade and #57 feedback as separate operations; selection originates from ME-09/#54 and returns to ME-09 after revalidation"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ME-10

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 worklogs of 198 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected requirements separate from current API/UI source; preserve source assets; current Study Web remains UNWIRED; don't claim UI runtime from API source or fake rows.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve screenshot/HTML divergence; describe exact filters/response source and pagination; no canonical UI-only skill; no browser route behavior is verified.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; trace each API caller→handler→query/side effect→response; mark declarations absent from runtime as not runnable; preserve linked-screen and API ordering discrepancies.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-10 only in this session. The goal objective requires a per-screen plan before marker/DD work, preserved original assets, ordered one-to-one markers, source-traced screen DD, tracker/worklog updates and independent `DD READY`, `IMPLEMENTATION BLOCKED`, `RUNTIME VERIFIED` status handling.
- Inventory row 50: proposed `/mentor/submissions/:submissionId`, AC-23, APIs #55/#56/#57. Read submission and file(s), enter score/rubric/feedback; keep grade and feedback as separate calls if API design splits them. Loading/dirty/grading/feedback-sent/conflict states; ME-09 is the predecessor/return screen.
- F09: ME-09/#54 → ME-10/#55 detail → #56 grade and #57 feedback. These mutations can succeed independently; show separate state and revalidate #55. Inventory flags rubric fields, score type and atomicity as unresolved.
- Skill routing: the registered `createDD-markdown` skill excludes `web-ui-only-dd`; there is no canonical skill for screen-level UI DD. Do not treat API DD template as UI behavior.

## CURRENT_BEHAVIOR

- At session start, the screen folder had the source `screen.png` and `code.html`; visual inspection shows the image is a complete 1600×1556 Mentor detail mockup. HTML has `href="#"` navigation, no fetch/API/network call, no action bindings for refresh/report/back/save, a disabled number input, empty rubric placeholder, and a feedback textarea whose only script behavior updates a character count.
- The screen mockup presents `PENDING_AUTH`, an example `SES-ME10-SYNC`/`SUB-VERIFYING` handoff, “AES-256”, “WCAG 2.1 AA”, a 0–100 disabled score field and a 0/0 rubric. These are design/sample copy; current source does not verify them as behavior, security posture, rubric data, or score contract.
- Study Web subcontext and current tree identify frontend source/package/router as `UNWIRED`; no editable screen implementation is present. No UI runtime claim is made.
- API #55–#57 routes and views exist in Study Server current source. Focused test modules exist and context records historical fake-DB coverage (#55: 22, #56: 27, #57: 28); tests were not run in this docs session. API DDs remain `Draft — Needs Confirmation`; source-backed local behavior and DERIVED fallbacks are not approved production contract or live schema evidence.

## SOURCE_TRACE

Expected chain from AC-23/F09: ME-09/#54 selection → proposed ME-10 path ID → GET #55 detail → independently submitted POST #56 grade and POST #57 feedback → client revalidates with GET #55. Current screen route/navigation is not wired.

- API #55: `apps/study-server/app/api/v1.py` composes `GET /api/v1/mentor/submissions/{submission_id}` with the #55 detail view. The shared MENTOR guard runs before path parsing/DB access; raw signed-int64 malformed/overflow path maps to 404; `FIND_MENTOR_SUBMISSION` reads candidate `assignment_submissions` with LEFT JOINs to `assignments`/`courses` and a LATERAL upload lookup constrained by exact `file_url`, Student owner, `SUBMISSION` purpose and course. Missing row is 404; broken required relation/projection is 500; another direct course owner is 403 (direct-owner rule DERIVED). It returns the reusable #54 `SubmissionResponse`, including at most one matched student upload; no rubric field/query exists. Success is 200 `DESIGN_RESOURCE_RETRIEVED`; read only, no commit.
- API #56: route → `grade_mentor_submission` → lock candidate submission/assignment/course (`FOR UPDATE`) → direct-owner check → validate strict `score:int32` against DERIVED `0 <= score <= assignments.max_score` → update `score` as `NUMERIC(6,2)` and `status='GRADED'`; preserve feedback; accept strict required `rubric_items:string` but do not persist it. It resolves the same constrained student upload, validates the response projection, then commits this mutation. Invalid path maps to 404; range to 422 `DESIGN_VALIDATION_ERROR`; other errors follow 401/403/404/500. No status precondition/409 source branch; regrading is currently possible.
- API #57: route → `save_mentor_submission_feedback` → shared MENTOR guard → malformed/overflow path maps to 422 `DESIGN_VALIDATION_ERROR` → lock row → direct-owner check → strict required `feedback_text:string` and `attachments:string` (extra fields forbidden) → update only `assignment_submissions.feedback`. `attachments` is not parsed, persisted, echoed, or exposed separately. Score/status are preserved; no `GRADED` precondition; repeated calls overwrite the single candidate feedback column. It resolves the same student-submission file projection, validates the `Submission` response, then commits separately from #56.
- Validation precedence: #56/#57 route functions declare required Pydantic body models. FastAPI body validation precedes invoking those route functions; the global `RequestValidationError` handler maps body errors on these design-contract paths to 422 `DESIGN_VALIDATION_ERROR`. Therefore malformed/missing/extra fields can return 422 before view-level MENTOR auth runs. The API catalog does not define this precedence; no unauthenticated-invalid-body test was run or claimed.
- Cross-screen API/DD evidence: `docs/lists/list_api.md` and #55–#57 API DDs all remain `Draft — Needs Confirmation`. #55 open questions say AC-23 requests rubric but the reusable response and legacy schema relation are absent; #56 open questions say score scale, rubric wire format/persistence, grade lifecycle and transaction sequencing require approval; #57 open questions say feedback attachment format/storage, overwrite/history, rubric response and Student visibility remain unresolved. The source's selected fallbacks are DERIVED.
- Current schema evidence: query.py targets legacy BIGINT `assignment_submissions`, `assignments`, `courses`, and `uploads`; checked-in DDL is only a candidate and live schema/deployment is not verified. #56/#57 own separate transactions, so the screen must expose partial success and must not imply cross-call atomicity.

## REVIEWED_SOURCE_FILES

- Screen source/assets and previous screen handoff: `apps/study-client/docs/screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/{screen.png,code.html}`, `apps/study-client/docs/screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/{ME-09.md,ME-09_PLAN.md}`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Project/scope/workflow context: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/INDEX.md`, `.agents/project/architecture.md`, `.agents/project/dependencies.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/INDEX.md`, `.agents/server-study/core/runtime.md`, `.agents/server-study/core/database-security.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/database.md`, `.agents/server-study/tests.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/context-manifest.json`.
- Requirement/contract sources: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`, `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`, `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio`, `docs/lists/list_api.md`, `apps/study-server/docs/dd/55_mentor_submissions_detail/OPEN_QUESTIONS.md`, `apps/study-server/docs/dd/56_mentor_submissions_grade/OPEN_QUESTIONS.md`, `apps/study-server/docs/dd/57_mentor_submissions_feedback/OPEN_QUESTIONS.md`, `infra/postgres/study-server/DB.sql`.
- Runtime source: `apps/study-server/app/api/v1.py`; #55 `models.py`, `validate.py`, `query.py`, `view.py`; #56 `models.py`, `validate.py`, `query.py`, `view.py`; #57 `models.py`, `validate.py`, `query.py`, `view.py`; shared #54 `models.py`; `apps/study-server/app/core/responses.py`, `apps/study-server/app/core/middleware.py`.
- Focused test source reviewed by context, not executed: `apps/study-server/tests/modules/mentor/api_55_mentor_submissions_detail/test_mentor_submission_detail.py`, `apps/study-server/tests/modules/mentor/api_56_mentor_submissions_grade/test_mentor_submission_grade.py`, `apps/study-server/tests/modules/mentor/api_57_mentor_submissions_feedback/test_mentor_submission_feedback.py`.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Rubric data | AC-23 says #55 reads rubric, but current #55 response/query has no rubric and #56 accepts but drops `rubric_items`. | DISCREPANCY / BLOCKED | Do not render an invented rubric or claim criteria were persisted. |
| Score input | Asset shows disabled 0–100; current #56 requires int32 and enforces DERIVED 0..assignment.max_score, with candidate NUMERIC(6,2) storage. | DISCREPANCY / BLOCKED | Contract must define scale, decimals, bounds and relationship to `max_score`; don't enable control by assumption. |
| Grade/feedback atomicity | F09 requires separate #56/#57 outcomes; each current API commits independently. | DERIVED SEPARATE TRANSACTIONS | Show partial completion distinctly; cross-call atomicity is absent and must not be implied. |
| Feedback attachments | Mockup has no clear attachment affordance; #57 requires opaque `attachments:string`, which current source ignores. | OPEN / BLOCKED | No upload/persistence behavior can be specified. |
| API access/schema/open questions | Direct-owner MENTOR policy, legacy nullable relations, file URL producer, attachment storage and live schema remain unapproved/unverified. | DERIVED / UNVERIFIED | Screen API behavior is source-traceable locally but not a closed production contract. |
| Body/auth response precedence | #56/#57 invalid Pydantic body can produce 422 before view-level MENTOR auth; API catalog does not state precedence. | CONTRACT GAP | Confirm behavior for malformed/missing/extra body fields when auth is absent/invalid. |
| Study Web screen runtime | No editable Study Web source/package/router exists. | UNWIRED | No ME-10 route or interaction can be runtime verified. |

## CHANGES

- Created `apps/study-client/docs/screen_stitch/04_mentor/ME-10_cham-diem-va-phan-hoi/ME-10_PLAN.md` before marker/annotation/DD artifacts.
- Created `ME-10_markers.json` (39 markers), `ME-10_markers_overlay.svg`, `screen_annotated.png` (2×, 3200×3112) and `ME-10.md` (A–F detailed design).
- Updated the ME-10 tracker row and current checkpoint in `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; filesystem count is 45/83 four-core artifact sets.
- No API implementation or context pages changed. Study Web remains UNWIRED; API tests and screen runtime were not run.

## VERIFICATION

- The selector selected three exact-type docs worklogs; all selected worklogs were individually read.
- Plan was written before marker map/overlay/annotated image/DD. Visual review of the full annotated image caught and corrected markers that initially covered navigation/title/control text; corrected version reviewed again.
- Static audit after the final edits: JSON parses; 39 sequential, unique IDs/numbers and all coordinates in 1600×1556 bounds; SVG has the exact same 39 IDs in order; 39 matching DD element rows; all 10 events have trigger/input/process/result coverage; all 32 relative Markdown links resolve.
- `screen_annotated.png` is 3200×3112 (2× dimensions and same aspect ratio as source). Original hashes remain `screen.png` `7ea38f3a02bbe2d4e136ff24c854435fa5946eb6ad148bf73e488058b5a7a41a`, `code.html` `fb1c5ddfdde5dbb47969aa39a4dca2b7ccfdb0bb64cd633d243a78e4690e03cc`.
- Static event audit: all 10 events have a trigger and a defined processing/result or explicitly no-op current behavior; the earlier literal-word checker was overstrict because an event need not contain the word “error”.
- Validation-order audit: #56/#57 route body annotations and `RequestValidationError` middleware confirm 422 can precede view-level auth; added as open contract question Q-ME10-11. This is source-derived behavior, not unauthenticated-invalid-body test evidence.
- `git diff --check`: PASS after the current documentation updates. No tests or runtime were run, per docs-only task scope.
- Separate screen status: `DD READY`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Mentor screen is ME-11, for a separate session.
