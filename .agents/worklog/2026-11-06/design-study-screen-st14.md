---
task_id: "2026-11-06-design-study-screen-st14"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-13 → ST-14 attempt handoff; API #28/#29 → #30 autosave; AC-16; G-09"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-14

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs selected of 175 exact-type `docs` worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve original assets; keep expected/current behavior separate; Study Web is UNWIRED; static prototypes do not prove routing or API behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Trace API contracts against current backend; keep UI/API discrepancies and unsupported behavior explicit; tests with fake sessions do not prove live runtime.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; current source outranks docs for runtime; do not invent routes, fields, data or navigation; keep DD/implementation/runtime statuses distinct.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Goal objective reread before continuing. This session handles ST-14 only, with plan before annotation/DD, original assets preserved, full marker map/DD, global tracker update and static audit.
- Inventory defines route `/student/quizzes/:quizId/attempts/:attemptId`, Student actor, AC-16, APIs #28/#29/#30, next screen ST-15, and question navigation, answer saving, optional server-provided timer and unanswered handling.
- Inventory sequence says POST #29 creates attempt, GET #28 loads per permission, PUT #30 saves answer changes; AC-16 depicts answer persistence and later submit. G-09 leaves answer representation/versioning, idempotency, timing/deadline and policy open.
- API catalog defines #28 GET quiz, #29 POST attempt with no body, #30 PUT answer with required `question_id:int64` and catalog notation `answer(s):string`; #30 response is `ApiEnvelope<QuizAttempt>` and has no catalog 409.
- AC-16 diagram associates eligibility denial with 403/409, #29 with attempt creation, #30 with answer upsert, #31 with submit and #32 with result; it does not resolve the client handoff ordering conflict.
- ST-13 current DD EV-02 says explicit Start sends #29 and only routes to ST-14 after 201 with a valid attempt ID. ST-14 inventory/F05 shorthand can be read as creating the attempt in ST-14. Do not call #29 twice; record the discrepancy for product/API resolution.

## CURRENT_BEHAVIOR

- ST-14 folder has only `screen.png` and `code.html`; source PNG is 1600×1468 RGB, SHA-256 `63ab0e25bd3c502d5f2ce699e93df046532a32862aa0256d3bb5bca1cae89cb8`; HTML SHA-256 `0579187c7347daaf9e48118f4422fef7dc719f00345f01b6f2fe1a15669afdfc`.
- The PNG is a design mockup of an in-progress quiz, with question 14/20, one selected choice, timer/counter/status widgets, navigation, question grid, and connection/instructor panels. Its “14/20” conflicts with 13 answered + 6 unanswered + 1 flagged; it displays two different timers. WebSocket ping, real-time/idempotent save claims, attempt count, and other sample values have no runtime proof.
- Companion HTML is a static fallback “Bài kiểm tra chưa sẵn sàng để làm”; it has no form, input, button, API, timer, or handlers. Its static exit/back anchors point to `/student/quizzes/:quizId`; they do not establish implemented routes and do not match the screenshot's loaded quiz state.
- Study Web has docs/assets and ignored compiled `dist` with only `/`; editable source, package/router and Student screen implementation are absent, and serving is unverified (`UNWIRED`).
- Study Server declared/current source supports APIs #1–#9, #12–#14, #34, #46–#98, not Student APIs #28–#32. Current route/module/test scan found no Student #28–#32 routes/modules/tests; Admin quiz endpoints #87–#91 are separate. Therefore no #30 caller/callee or runtime database write exists to trace; candidate API/DB documents are design evidence only.
- API #30 DD is Draft/Needs Confirmation. Catalog notation does not specify a usable JSON answer property/representation; reusable logical answer alternatives are not aligned with the catalog string. Candidate `quiz_answers` DDL has one `choice_id`, `is_correct NOT NULL`, `score_received`, no text-answer column and no uniqueness on `(attempt_id, question_id)`; table design and DDL also disagree on FK nullability. No transaction, upsert key, concurrency/retry/idempotency, ownership/state/expiry rules, response projection or answer disclosure policy is settled.

## SOURCE_TRACE

- Screen inventory: `apps/study-client/docs/list_screen.md` ST-14, F05, API index and G-09 rows; route/actor/API/next-screen and state inventory reviewed.
- UI source: `apps/study-client/docs/screen_stitch/03_student/ST-14_lam-bai-kiem-tra/{screen.png,code.html}`; both retained unchanged. HTML static anchors inspected; no executable Study Web source exists to trace.
- Cross-screen handoff: `apps/study-client/docs/screen_stitch/03_student/ST-13_gioi-thieu-bai-kiem-tra/ST-13.md` EV-02 was reviewed; it invokes #29 on explicit Start and passes a returned attempt ID into ST-14.
- API/AC evidence: `docs/lists/list_api.md` #28–#31 and logical schemas; `apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio` AC-16 flow; API #30 DD `03_Request.md`, `05_Data_Mapping.md`, `06_Error.md`, `OPEN_QUESTIONS.md`.
- Database/source evidence: `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` answer model and `infra/postgres/study-server/DB.sql` candidate DDL. No live schema or #30 implementation is claimed.
- Current implementation boundary: `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `apps/study-server/app/api/v1.py`, app modules and tests scan; no Student #28–#32 endpoint/caller/test found. `.agents/web-work/study/INDEX.md` confirms Study Web is unwired.
- Scope context and design target read: `.agents/web-work/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/INDEX.md`, `.agents/web-study/design.md`; `web-ui-only-dd` is not a canonical wired skill in `.agents/context-manifest.json`, so no skill applies to this UI-only DD.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST14-D01 | ST-13 EV-02 says #29 occurs on Start before ST-14; ST-14 row/F05 shorthand can imply #29 occurs in ST-14. | `DISCREPANCY / BLOCKER` | Do not create a second attempt; owner must define the single trigger and route handoff. |
| ST14-D02 | PNG is loaded quiz UI while HTML is unavailable fallback with no matching controls/handlers. | `DISCREPANCY` | Neither visual state nor static anchors prove runtime behavior. |
| ST14-D03 | Study Web lacks editable source/router and Student UI; Study Server lacks Student #28–#32 routes/modules/tests. | `UNWIRED / NOT_FOUND / DECLARED_NOT_RUNNABLE` | No runtime behavior or route/API integration is verified. |
| ST14-D04 | #30 catalog answer notation, logical model, candidate physical schema, and draft DD do not agree; key, concurrency, ownership/state and response policy remain open. | `BLOCKER — API/DB contract` | Cannot finalize answer payload, autosave sequencing/recovery, mapping or safe response. |
| ST14-D05 | Mockup has divergent progress totals/timers and unsupported WebSocket/idempotent-save/sample claims. | `DESIGN_ONLY / SOURCE_REQUIRED` | Do not encode these claims as expected runtime behavior. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-14_lam-bai-kiem-tra/ST-14_PLAN.md`, `ST-14.md`, `ST-14_markers.json`, `ST-14_markers_overlay.svg`, `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog. Original `screen.png` and `code.html` were not changed.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: #29 trigger remains unresolved; plan/DD preserve source conflict and avoid double invocation. DD/implementation/runtime statuses stay distinct.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Objective/context/worklog preflight | Objective reread; router/context map/worklog contract read; 3 selected exact-type worklogs read. | VERIFIED |
| ST-14 source and contract inspection | Asset hashes/dimensions; inventory/API/AC/ST-13 handoff; API #30 DD/candidate DB; Study Web and Study Server current implementation boundary reviewed. | VERIFIED |
| `render_annotation.py ... --scale 2` | Rendered 32 markers at 3200×2936 from unchanged 1600×1468 source; inspected placement and moved marker #13 out of question heading. | VERIFIED |
| Static consistency audit | Original hashes unchanged; marker sequence/bounds and 1:1 map verified; SVG parsed with 32 markers; DD/plan relative links resolve; 83 IDs/folders and 23 complete artifact sets; tracker updated to 23/83 and next pointer ST-15. | VERIFIED |
| `git diff --check` + new-file whitespace audit | No whitespace errors. | VERIFIED |

## HANDOFF

- Remaining blockers: #29 trigger/handoff; #30 answer schema/upsert/access/state/response/retry policy; attempt resume and timer source; unavailable Student runtime implementation; design/source mismatch and unsupported mockup claims. ST-14 is `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`.
- Next owner/action: begin ST-15 in the next independent session; ST-14 work stops at this screen.

