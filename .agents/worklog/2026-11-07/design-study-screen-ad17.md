---
task_id: "2026-11-07-design-study-screen-ad17"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-35; API #91; AD-15 → AD-17 statistics handoff; API #91 catalog ↔ Study Server source"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-17

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 222; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; keep Study Web `UNWIRED`; distinguish catalog, source and runtime; no unsupported dashboard/analytics fields or runtime claims.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Read registry for skill applicability; no canonical UI-only DD skill; preserve original assets; source/test presence does not prove runtime or live schema.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Maintain API/UI status distinction, trace current route/query/response/test source, and retain role/schema/PII discrepancies without inferring from mockup.
- additional handoff reviewed: `.agents/worklog/2026-11-07/design-study-screen-ad16.md` — AD-16 completed in its own session; next Screen ID is AD-17; API #91 catalog `ApiEnvelope<Quiz>` differs from local `QuizStatistics` source; API DD remains Draft; preserve AC-35 permission and live schema blockers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-17 only for this session under the active 83-screen goal. Read inventory row 75, AC-35, API #91 catalog/Draft DD and current server source/tests; write `AD-17_PLAN.md` before markers, annotation or screen DD; preserve source assets; produce ordered one-to-one markers, `screen_annotated.png`, A–F DD, tracker/global-plan updates and this worklog; run the required static audit; do not start another Screen ID.
- AD-17 is the AC-35 statistics handoff from AD-15. Exact actor, route, metrics, filters and navigation must be confirmed from current inventory/diagram/API evidence before authoring.
- The API #91 direct contract, current server behavior, data source and any metric formulas must remain separately labeled. Do not invent analytics fields or infer statistics from #87 Quiz metadata.

## CURRENT_BEHAVIOR

- Target folder `apps/study-client/docs/screen_stitch/05_admin/AD-17_thong-ke-bai-kiem-tra/` initially contains only `screen.png` (1600×1440, SHA-256 `7df0306c1b757d8c0af0cbe56e382ed2bfe77c9a82598d98d1af9607df55de19`) and `code.html` (18,554 bytes, SHA-256 `9346a0bc0b34b861b9fe6e0c1e6627e2e094ed04219ffc335954f671fe2df4b3`). The screenshot is a blank analytics state; no chart, attempt data, distribution or duration metric is visible.
- HTML contains the Admin shell and static page text. The only active listener is `btnCheckConnection`: it disables the button, changes its label/spinner, waits 700 ms, displays static “Kết nối API hoạt động bình thường…Trống Analytics” feedback, then resets the label after 3 seconds. It does not make a network call. Shell `href="#"` links are placeholders. The breadcrumb and two visible back links point to `/admin/quizzes`.
- Current Study Web checkout has `docs/`, `dist/`, `node_modules/` and `tsconfig.tsbuildinfo`; no editable app source, package manifest, client router, API client or AD-17 implementation was found. Current frontend routing/runtime is therefore `UNWIRED` / `NOT VERIFIED`.
- Study Server has an actual local #91 route and module (`app/api/v1.py`, `app/modules/admin/api_91_admin_quizzes_statistics/{models,validate,query,view}.py`) plus HTTP test source. Route is GET `/api/v1/admin/quizzes/{quiz_id}/statistics`; shared Bearer/JWT `ADMIN` guard runs before positive signed-int64 parsing and DB access. Query is a read-only grouped `LEFT JOIN` over legacy `quizzes`/`quiz_attempts`; `quiz_id`, `passing_score`, attempt `id`, `submitted_at`, `score` are read; no `quiz_answers`, status filter, commit or write. Local response is a derived `AdminQuizStatistics` with `attempt_count`, `submitted_attempt_count`, `graded_attempt_count`, `average_score`, `passed_attempt_count`, `pass_rate_percent` (plus `quiz_id`). SQLAlchemy/mapping errors roll back and return 500; missing/malformed ID maps to 404; auth errors map to 401/403. Local source does not provide score distribution, completion rate or average attempt duration.
- Metric formulas/NULL semantics and the separate `QuizStatistics`-style response remain DERIVED proposals in API #91 DD; API DD status is `Draft — Needs Confirmation`. Existing backend verification report (2026-11-01) records the #91 success path as PASS; tests were read, not run in this session. Fake-DB tests and that report do not verify live PostgreSQL schema, deployed route or fine-grained permission.
- Current worktree already has prior documentation changes in `apps/study-client/docs/list_screen.md` and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; preserve and update only the AD-17 rows/checkpoint needed.

## SOURCE_TRACE

```text
Expected: list_screen.md row 75 + AC-35 node n4/edge STATISTICS → n11 GET #91 → n12 Aggregate attempt statistics → n13 display; actor Admin with quiz-management permission; AD-15 is the entry/return screen. Direct catalog #91 requires Bearer JWT, role=Admin and path quiz_id:int64!, declares `ApiEnvelope<Quiz>`, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/404/500, and no body/query.
Current API source: Study Server route #91 → shared ADMIN guard → positive int64 parser → one read-only grouped legacy BIGINT quizzes/quiz_attempts aggregate → derived `AdminQuizStatistics` envelope. Local metric field/formula assumptions are not approved API contract. API DD documents exact conflicts and owner questions; no client caller/runtime is present in Study Web.
Current screen prototype: static shell → route parameter placeholder `:quizId` and no bound Quiz → empty analytics statement → AD-15 link or cosmetic timer button. No API call, auth guard, response parser, rendered statistics or actual connectivity check exists in HTML.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-35 actor vs current auth | AC-35 precondition is Admin with quiz-management permission; local #91 checks only shared `ADMIN`. No fine-grained policy source found in #91 DD. | DISCREPANCY / SOURCE_REQUIRED | Do not claim the local role guard satisfies quiz-management permission. |
| API #91 direct response vs current local response | `docs/lists/list_api.md` direct contract is `ApiEnvelope<Quiz>`; local route response model is `GetAdminQuizStatisticsEnvelope` containing a separate `AdminQuizStatistics` DTO. | DISCREPANCY | Cannot map direct contract to analytics values; retain catalog as direct and local DTO as DERIVED pending owner approval. |
| Metric meaning and coverage | AC-35 only says “Aggregate attempt statistics”. Local proposal uses all matching attempts, submitted_at, score and passing_score. Mockup additionally claims score distribution/completion rate/average duration, which local #91 does not return. | DERIVED / BLOCKER | Do not invent these values or claim chart/readiness; document candidate local fields separately and request contract approval. |
| Metric / DB semantics | Local SQL reads legacy BIGINT `quizzes`/`quiz_attempts`, includes rows without status filters, and does not read `quiz_answers`; V1-PILOT UUID model differs. Live schema and tombstone/nullability policy are unverified. | SOURCE_REQUIRED / BLOCKER | Keep candidate formulas and table projection traceable; no claim of deployed or production statistics. |
| AD-17 route and UI behavior | Inventory route is `/admin/quizzes/:quizId/statistics`; source HTML only shows `:quizId` placeholder, has no route/router/API call. | UNWIRED | Document route as candidate; do not claim navigation or request is implemented. |
| Empty state and connection button | Empty copy claims analytics service unconfigured; active click only runs a timer and then shows fixed API-success text. | STATIC_ONLY / DISCREPANCY | Label these as mockup behavior, not network state or API evidence. |

## CHANGES

- Saved `AD-17_PLAN.md` after the complete evidence review and before creating markers, annotation or DD. Created 33 marker JSON/SVG entries, 2× annotated PNG, and A–F DD with 33 element rows and nine detailed events. Updated inventory row 75, reverse API #91 status, G-11, global AD-17 plan row/checkpoint, and this worklog. Original `screen.png` and `code.html` were not edited.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none. Route/metric/permission/schema decisions remain explicitly marked candidate, DERIVED, discrepancy or blocker.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Active goal and objective requirements reviewed; router, context map, worklog contract/template, relevant project/scope pages and registry routing reviewed; exact docs selector READY 3/222; AD-01/02/03 and AD-16 worklogs read. | VERIFIED |
| AD-17 source and contract trace | Inventory row 75, AC-35 diagram, #91 direct catalog and Draft DD, Study Web tree, screenshot/HTML, Study Server route/module/query/model/validator/view and test source reviewed. | VERIFIED_SOURCE_REVIEW |
| Existing API verification evidence | `docs/testing/api-test-report-2026-11-01.md` records #91 success path PASS; no tests run in this screen-design session. | VERIFIED_REPORT / NOT_RUN_THIS_SESSION |
| Plan-before-assets order | `AD-17_PLAN.md` was saved before marker JSON/SVG, annotated PNG and DD. | PASS |
| Static artifact audit | 33 markers sequential/unique/in-bounds/non-overlapping; JSON/SVG/DD coordinates match; SVG XML/JSON parse; annotated PNG is 3200×2880; original image is 1600×1440; original image/HTML hashes unchanged; 22 DD links resolve; A–F and 33 element rows present; 83/83 screen IDs/folders, 70/83 core artifact sets. | PASS |
| Visual annotation review | Full annotated image inspected; marker numbers are legible, targets identifiable, and content is not obscured. | PASS |
| Whitespace / repo diff | `git diff --check` passed; new AD-17 text artifacts have no trailing whitespace. | PASS |
| Agent context validator | `node scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID`; report includes missing db-admin context/source paths and stale server-study source fingerprints. No context page or source code was changed for AD-17. | REPOSITORY_CONTEXT_FAILURE_OUTSIDE_AD-17 |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining work in this session: none. AD-17 artifacts, trackers and static audit are complete; do not start another Screen ID in this session.
- Remaining blockers: approved statistics response/metrics, AC-35 permission policy vs shared ADMIN, legacy/live schema and deployment verification, missing Study Web wiring, and static-only mockup copy/control.
- Next Screen ID for a separate session: AD-18.
