---
task_id: "2026-11-06-design-study-screen-st16"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-15 → ST-16 result handoff; API #31 → #32; AC-16; G-09"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-16

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 selected of 177 exact-type docs worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Separate target behavior from current source; do not infer route, data or runtime from screenshot/HTML; keep Study Web UNWIRED explicit.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Preserve asset/API discrepancies; trace server source separately from catalog and avoid promoting mock values to data contract.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Preserve AC-vs-inventory orchestration discrepancies; distinguish SOURCE_BACKED from catalog D labels and UNWIRED UI; do not infer enrollment or route behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Re-read `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; this session handles ST-16 only, writes its plan before marker/DD work, preserves originals, creates the annotation/marker map/DD, updates tracker/worklog and keeps DD, implementation and runtime statuses distinct.
- Inventory row ST-16: Student result page at `/student/attempts/:attemptId/result`, AC-16, API #32, links ST-09 and ST-20, states `pending/graded/unavailable/error`. GET #32 after submit; pending grading must display status and must not be treated as score 0. Do not expose answers outside approved policy.
- API catalog #32: `GET /api/v1/attempts/{attempt_id}/result`, Student Bearer JWT, required `attempt_id:int64` path only, no query/body; response `ApiEnvelope<QuizAttempt>`. Success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/404/500. AC-16 sends both AUTO GRADED and PENDING GRADE branches to #32 and describes reading score + feedback/status.
- API #32 DD is `Draft — Needs Confirmation`. Open questions cover owner/masking, read availability and PENDING_GRADE fields, answer disclosure, feedback source, answer mapping/order and path validation. The logical `QuizAttempt` has status/timestamps/optional score/answers, but no feedback or quiz title, passing result, skill metrics or next-module fields.
- Static screenshot claims (90%, pass, GPA A+, 2/3 attempts, skill scores, per-question correctness/mentor feedback, next lesson unlock and PDF) are not established by the #32 contract. Values are sample design content until sourced/approved.

## CURRENT_BEHAVIOR

- `screen.png`: 846×1600 RGB; SHA-256 `aa6a8e5326eab69ea6d224b45be4c7d3b880ecf0e55c9ac20647bd0baa15fcb7`. It is a loaded-result mockup with pass badge, React Hooks title, duration/submitted time/attempt ordinal, next-lesson unlock, 90%/18 of 20 and 9/10/GPA A+, three skill cards, question filters, two review cards showing correct answers/feedback/video links, and a next-module/PDF action card. These values and claims are not current server data.
- `code.html`: 10,503 bytes; SHA-256 `ba551f83e6419b915d62d193a7ec15aade4ecd2cfe493b996514a1ccd7682237`. It is a Guest header plus generic “result not ready” state and “Quay lại khóa học” link. It contains no API call or route-bound data. Script targets `.review-tab-btn` and `.question-card`, both absent from this HTML DOM; screenshot's review interactions are therefore not represented by the companion HTML.
- Study Web current source inventory has docs/assets and an ignored compiled `dist` artifact only; no editable app source, package manifest, entrypoint or Student route. Serving/deployment is unverified (`UNWIRED`).
- API catalog/API #32 DD exist, but exact route search in `apps/study-server/app/api/v1.py`, `app/modules/`, `tests/` and `.agents/server-study/apis/declared-routes.md` finds no Student `GET /api/v1/attempts/{attempt_id}/result`; no API #32 module or test is present. Admin quiz APIs #87–#91 are separate routes and do not provide Student result access. API #32 remains `NOT_FOUND / UNWIRED / DECLARED_NOT_RUNNABLE` as runtime behavior.
- API #32 DD status is `Draft — Needs Confirmation`; it proposes candidate `quiz_attempts`/`quiz_answers` reads and owner comparison but explicitly leaves SQL, owner masking, result-state predicate, ordering and response projection unresolved.
- Checked-in candidate DDL has nullable `quiz_attempts.submitted_at` and `score`, `status VARCHAR(20) DEFAULT 'IN_PROGRESS'` without canonical enum, `quiz_answers.is_correct NOT NULL`, and `score_received DEFAULT 0`; it has no feedback column or text-answer column. This is design evidence only, not live schema.

## SOURCE_TRACE

- `apps/study-client/docs/list_screen.md`: ST-16 row, F05 sequence and G-09; ST-15 → ST-16 after API #31 submit, then GET #32; related screens ST-09/ST-20.
- ST-16 `screen.png`/`code.html`: original hashes/dimensions above; visual loaded state conflicts with HTML unavailable state; static HTML has no #32 request or results DOM.
- `docs/lists/list_api.md` API #32 row and reusable `QuizAttempt`/`QuizAnswer` definitions; API #32 DD `00_Cover.md`, `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md`.
- `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md` AC-16 and `AC_02_STUDENT_LEARNING.drawio`: Student precondition; AUTO GRADED and PENDING GRADE branches converge to GET #32; diagram says read score + feedback/status. Inventory/API DD do not resolve the fields/policy.
- API #31 `OPEN_QUESTIONS.md`/`04_Response.md`: submit grading formula/state and answer response/disclosure remain open; ST-15 DD requires #32 after accepted #31 success but does not provide result state payload.
- `apps/study-server/app/api/v1.py`, `app/modules/`, `tests/`, `.agents/server-study/apis/declared-routes.md`: exact Student #32 route/module/test search returns no match. Admin quiz routes are separate.
- `infra/postgres/study-server/DB.sql` and `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md`: candidate tables/fields only; no live schema claim.
- `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-study/design.md`: Study Web `UNWIRED`; accessibility/layout guide is intended target only.
- Registry check: `.agents/context-manifest.json` and `.agents/skills/INDEX.md` exclude `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only DD skill applies.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST16-D01 asset mismatch | Screenshot is detailed loaded result; HTML is generic unavailable state with Guest sign-in/register header and course-list link. | `DISCREPANCY` | Preserve both originals; neither proves current runtime. |
| ST16-D02 Student route/API | Study Web has no editable route; API #32 has catalog/DD but no current Student route/module/test. | `UNWIRED / NOT_FOUND / DECLARED_NOT_RUNNABLE` | No result UI/network/DB behavior is runtime-verified. |
| ST16-D03 response/design gaps | #32 `QuizAttempt` lacks quiz title, pass/GPA, skill aggregation, question content, feedback and next-module data. | `BLOCKER — source/contract required` | Do not infer screenshot score/pass/skill/review/unlock/PDF claims. |
| ST16-D04 grading states | AC-16 sends both `GRADED` and `PENDING_GRADE` to #32; score null/omit/partial and other status behavior are unresolved. | `BLOCKER — API #32 Q-32-02` | Render waiting state from approved status; do not treat pending as score 0 or final grade. |
| ST16-D05 disclosure/feedback | API #32 Q-32-03/04 leaves per-answer correctness/score and feedback source unresolved; screenshot reveals answer key and mentor feedback. | `BLOCKER — policy/schema` | Do not expose answer correctness, key or feedback before explicit approved policy/source. |
| ST16-D06 ownership/validation/mapping | Q-32-01/05/06 leaves owner 403/404, availability, answer shape/order and path error mapping open. | `BLOCKER — API owner` | Do not invent alternate error codes, answer order or owner masking. |
| ST16-D07 navigation actions | Screenshot's PDF, review, next lesson unlock/module actions are not in ST-16 inventory/API #32; HTML links only to `/student/courses`. | `DESIGN_ONLY / UNWIRED` | Do not add routes, report generation or progress writes; get approved destination/data source. |

## CHANGES

- Created `ST-16_PLAN.md` before marker, annotation, and DD authoring; it records the asset baseline, 38-element plan, event flow, contract gaps, and acceptance checks.
- Created `ST-16_markers.json`, `ST-16_markers_overlay.svg`, and `screen_annotated.png` with 38 ordered badges aligned to target rows in the side gutters; `screen.png` and `code.html` were preserved.
- Created `ST-16.md` with sections A–F, 38 one-to-one element mappings, six events, API/state/error/navigation/accessibility handling, and explicit blockers.
- Updated the master tracker: ST-16 is DD BLOCKED / IMPLEMENTATION BLOCKED / RUNTIME NOT VERIFIED; complete artifact sets are 26/83; next screen is ST-17.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective and docs preflight | Re-read the objective file; `node scripts/select-worklogs.mjs --type docs --limit 3` returned READY, 3/177 exact-type docs worklogs, and all three selected logs were read. | VERIFIED |
| Original asset baseline | `screen.png` remains 846×1600 RGB, SHA-256 `aa6a8e5326eab69ea6d224b45be4c7d3b880ecf0e55c9ac20647bd0baa15fcb7`; `code.html` remains 10,503 bytes, SHA-256 `ba551f83e6419b915d62d193a7ec15aade4ecd2cfe493b996514a1ccd7682237`. | VERIFIED |
| Marker/DD map | Static Python audit found markers #1–#38 in sequence, unique `ST16-EL-01`…`ST16-EL-38`, in-bounds target/badge coordinates, and exact ordered match to all 38 DD element rows. | VERIFIED |
| Annotation render | SVG parsed with 38 number labels; annotation canvas metadata is 1008×1600 at scale 2; all target and badge coordinates are in bounds, badge rows align to target rows, and badges do not overlap; `screen_annotated.png` is 2016×3200. | VERIFIED |
| Markdown links and inventory | All relative links in `ST-16.md` and `ST-16_PLAN.md` resolve. Static inventory check found 83 unique screen IDs and folders, 26 complete six-file artifact sets and 57 incomplete sets; ME-01 is counted from file presence only and was not reviewed in this session; tracker ST-16 row and ST-17 pointer agree. | VERIFIED |
| Whitespace check | `git diff --check` and explicit whitespace scan on the new/updated text files reported no issues. | VERIFIED |
| Runtime/tests | No tests or runtime checks were run; no runtime behavior is claimed. | NOT RUN |

## HANDOFF

- Remaining blockers: API #32 is still a draft with no Student route/module/test; owner masking, path validation, result availability/status mapping, pending score projection, answer/correctness disclosure, answer shape/order, and feedback source need approved contracts. Screenshot score/pass/skill claims and PDF/course-outline/next-lesson actions lack source contracts; screenshot and HTML represent different actors/states; Study Web is UNWIRED.
- Next screen: ST-17, in a separate session. Do not process another Screen ID in this session.
