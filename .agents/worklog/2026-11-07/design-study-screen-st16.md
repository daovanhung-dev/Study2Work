---
task_id: "2026-11-07-design-study-screen-st16"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-15 #31 submit → ST-16 #32 result; AC-16 grading outcomes; related ST-09/ST-20 result presentation"]
status: "IN_PROGRESS"
---

# Worklog: Detailed Design màn hình Study ST-16

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 243; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; trace server auth, query/effects, response and tests; do not infer runtime from mockups or catalog; distinguish DD/implementation/runtime status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not expand fields or actions from mockup; preserve catalog/source discrepancies and user/data policy blockers; fake DB tests do not prove live schema/deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use only approved API/source fields; keep permission, privacy and lifecycle decisions open; source-backed local implementation is not runtime proof.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st15.md`
    - carry_forward: ST-15 hands off to ST-16 only after accepted #31 response; #31 remains Draft with ownership/state/repeat/deadline/grading/transaction/response questions open; AC-16 has `PENDING_GRADE`/`GRADED` outcomes; Study Web and Student #30–#32 remain unwired/not found; preserve schema/model discrepancies and sample-only score/skill claims.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-16 only this session; inspect current inventory, contracts, assets and implementation; write/re-audit ST-16 plan before DD/tracker edits; preserve source assets; verify marker ↔ element mapping; produce traceable A–F DD; update only ST-16 in the inventory and global tracker plus this worklog; keep DD, implementation and runtime statuses separate.
- Canonical inventory: `apps/study-client/docs/list_screen.md` ST-16 row and F05 say route `/student/attempts/:attemptId/result`, AC-16, API #32, related ST-09/ST-20, and pending/graded/unavailable/error states. F05 sequence is GET #28 → eligibility → POST #29 → PUT #30 → POST #31 → GET #32; ST-16 must follow an accepted #31 result.
- AC-16 design: both `AUTO GRADED` and `PENDING GRADE` branches reach #32, then read score + feedback/status. The AC does not settle the #32 response projection, pending score visibility, feedback source, or answer disclosure policy.
- API catalog #32 design contract: `GET /api/v1/attempts/{attempt_id}/result`, Student Bearer, required `attempt_id:int64`, no query/body, `ApiEnvelope<QuizAttempt>`, success 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/404/500. API #32 DD is Draft; Q-32-01…06 remain open for ownership/masking, pending availability/score, correctness disclosure, feedback source, answer shape/order, and path/error mapping.
- Canonical UI target: `.agents/web-study/design.md` specifies ocean tokens, Inter/system font, restrained surfaces, responsive widths, and 44px minimum controls. The supplied screenshot/HTML are design inputs and are not runtime proof.

## CURRENT_BEHAVIOR

- Study Server source and declared route inventory contain no Student #32 result route/module/test; current feature source for #32 is `NOT_FOUND`. Study Web has no source `src/` tree or package manifest and its scope status is `UNWIRED`; no runtime verification is available.
- The supplied `screen.png` is a populated Student result mockup. `code.html` is a Guest/unavailable state with login/register and a course link; it performs no API request. Its `.review-tab-btn` and `.question-card` selectors match no DOM elements. Thus the assets disagree on actor and state.
- API #32 logical `QuizAttempt`/`QuizAnswer` fields omit quiz title, pass threshold, GPA, skills, question content/options, feedback, next module and PDF data. Screenshot values/actions have no source contract.
- Legacy Study Server DDL uses BIGINT quiz attempts/answers; V1-PILOT uses UUID assessment attempts with a submitted snapshot and different immutable answer storage. These are competing design candidates; live schema and the API adapter are unverified.
- Current design artifacts also differ from `.agents/web-study/design.md`: PNG uses dense navigation/small type and cobalt/green gradients; HTML loads remote Plus Jakarta Sans, Material Symbols and Tailwind CDN and shows a separate composition.

## SOURCE_TRACE

```text
Repository context: root AGENTS.md, .agents/AGENTS.md, .agents/context-map.md, .agents/project/INDEX.md and relevant project pages; web-work and server-study scope entry/index pages; .agents/context-manifest.json and .agents/skills/INDEX.md confirm no wired canonical skill for web UI-only DD.
Preflight: scripts/select-worklogs.mjs --type docs --limit 3 selected and all three exact-type logs AD-01, AD-02, AD-03 were read; ST-15 dependency worklog was also read.
Expected flow: apps/study-client/docs/list_screen.md ST-16 row and F05; AC-16 node/branches in apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio and its API index; API catalog in docs/lists/list_api.md.
API #32 design: apps/study-server/docs/dd/32_attempts_result/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md; API #31 dependency questions in apps/study-server/docs/dd/31_attempts_submit/OPEN_QUESTIONS.md.
Current implementation evidence: apps/study-server/app/api/v1.py and .agents/server-study/apis/declared-routes.md search has no #32 result path; Student route/module/test search has no #32. .agents/web-work/study/INDEX.md marks Study Web UNWIRED; checkout has no apps/study-client/src or package.json; ignored dist inspection did not identify an ST result route or #32 path.
Storage candidates: apps/study-server/docs/diagrams/DB_UNICA_TABLES.md, infra/postgres/study-server/DB.sql (legacy BIGINT), infra/postgres/02_study_db.sql (V1-PILOT UUID assessment model). These are not live-schema evidence.
Design/assets: .agents/web-study/design.md; ST-16 screen.png (846x1600, SHA-256 aa6a8e5326eab69ea6d224b45be4c7d3b880ecf0e55c9ac20647bd0baa15fcb7); code.html (10,503 bytes, SHA-256 ba551f83e6419b915d62d193a7ec15aade4ecd2cfe493b996514a1ccd7682237); screen_annotated.png (2016x3200); ST-16 markers JSON/SVG and A-F DD.
Static audit after edits: inventory 83 IDs / 83 screen folders; 82 six-artifact bundles, ST-01 incomplete and ST-16 complete; 38 JSON markers = 38 SVG groups = 38 DD rows; unique/in-bounds target coordinates; SVG badge centers match JSON; DD/plan local links 26/20 all resolve.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #32 design vs current route | Catalog/API DD #32 Draft with Q-32-01…06; no Student route/module/test or Study Web implementation found. | DISCREPANCY | DD remains blocked; no runtime claim. |
| Result state and data disclosure | AC-16 names GRADED/PENDING_GRADE; pending score, answer/correctness exposure, feedback and projection/order are unresolved. | BLOCKER | Do not synthesize score/pass or expose answer key/feedback. |
| Attempt storage/model | Legacy BIGINT quiz-attempt schema differs from V1-PILOT UUID assessment-attempt/snapshot model; no approved adapter/live schema proof. | DISCREPANCY | Do not infer source table or cast identifiers. |
| Visual source and design target | PNG loaded Student result conflicts with Guest/unavailable HTML and Study Web design guidance; screenshot data/actions lack API source. | DISCREPANCY | Canonical state and field/action sources must be resolved. |
| Inventory completeness | 83 unique IDs/folders; 82 have all six assets, ST-01 incomplete; ST-16 has all six. | VERIFIED | No other screen ID edited. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_PLAN.md` (re-audit/source links/static closure); `ST-16.md` (database and design-system discrepancies, blockers, checklist, source links); `apps/study-client/docs/list_screen.md` (ST-16 row and F05 result handoff); `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ST-16 row and checkpoint); this worklog.
- Existing `screen.png`, `code.html`, `ST-16_markers.json`, `ST-16_markers_overlay.svg`, and `screen_annotated.png` were not edited. No other Screen ID, API DD, DDL, or context page changed.
- CONTEXT_UPDATES: none; no source/contract/global context page changed.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; selected and fully read AD-01, AD-02, AD-03; also read ST-15 dependency worklog. | VERIFIED |
| `python3 - <<'PY'` (inline static audit) | Source PNG/hash and HTML size/hash match plan; PNG 846×1600 and annotated PNG 2016×3200. 38 sequential JSON markers, 38 DD rows and SVG groups; badge centers match JSON; target coordinates unique/in-bounds; A–F headings and six event definitions present; 26 DD and 20 plan local links all resolve. | VERIFIED |
| Inventory/folder/core-artifact audit (Python stdlib) | 83 unique Screen IDs, 83 folders; 82 have the six core artifacts (only ST-01 incomplete); ST-16 has all six. | VERIFIED |
| `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md apps/study-client/docs/screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16.md apps/study-client/docs/screen_stitch/03_student/ST-16_ket-qua-bai-kiem-tra/ST-16_PLAN.md` | No whitespace errors in tracked files. Separate whitespace scan also found no trailing spaces in the ST-16 DD, plan or worklog. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: missing db-admin context pages/source roots plus `CONTEXT_STALE` across server-study/server-work/web-work/mobile-work/db-admin; repository-wide existing baseline, unrelated to this ST-16 change. | FAILED (pre-existing) |
| Application tests/runtime/live DB | Not run, as required by the per-screen static-audit plan; no runtime or live-schema claim. | NOT RUN |

## HANDOFF

- Remaining blockers: API #32 route/response and Q-32-01…06; disclosure/feedback and pending-score policy; legacy/V1-PILOT schema mapping and live schema; canonical loaded/unavailable UI state and design alignment; unsupported screenshot claims/CTA destinations; Study Web remains UNWIRED.
- Status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next owner/action: ST-17 in a separate session after ST-16; do not start another Screen ID in this session.
