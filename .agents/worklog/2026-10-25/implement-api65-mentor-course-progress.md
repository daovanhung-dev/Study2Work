---
task_id: "2026-10-25-implement-api65-mentor-course-progress"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETE"
---

# Worklog: Implement Study Server API #65 Mentor course progress

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 58 matching worklogs available; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Use the legacy BIGINT upload relation only when the progress flow has an explicit asset link; checked-in migrations are not live schema evidence.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Mentor lecture creation targets legacy BIGINT `lessons`, sets `PUBLISHED`, and checks direct course ownership; its local DDL is not live deployment proof.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Trace the #47 producer's persisted lesson/assets before deriving progress joins; preserve the raw int64 path/error contract and use query constants plus view orchestration.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [docs, test]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Implement API #65 from its DD for AC-26, review logically linked APIs #66/#67 and producer APIs #46/#47/#48, write a detailed plan before runtime edits, then verify the route with HTTP tests.
- Catalog contract (preliminary, to verify against current catalog/DD): `GET /api/v1/mentor/courses/{course_id}/progress`; Bearer JWT with MENTOR role; required `course_id:int64`; no query/body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Page<Course>>`; exact errors 401/403/404/500.
- User conflict order: AC diagrams → checked-in infrastructure → API catalog → simplest coherent DERIVED fallback if conflicts remain. Keep direct contract distinct from derived progress projection and retain DD Draft status unless source provides approval.

## CURRENT_BEHAVIOR

- API #65 DD existed at `apps/study-server/docs/dd/65_mentor_course_progress/` and reported `UNWIRED / NOT_FOUND` before this implementation.
- DD says AC-26 separates #65 class-level progress from #66 learning-event analytics and #67 selected-Student progress. The direct catalog `Page<Course>` response has a conflict with the progress purpose and no pagination parameters.
- Pre-edit source check: no API #65 module, router operation, middleware allowlist entry, or focused test existed. APIs #66/#67 remain absent and review-only in this task.
- API #62 runtime provides the closest roster/access precedent: `validate_current_user_request(..., role="MENTOR")`, numeric token `sub`, `courses.mentor_id` direct ownership, active enrollments, `users.role='STUDENT'`, distinct users, and read-only query flow. Its owner check precedes roster query.
- API #9 runtime filters curriculum to `lessons.status='PUBLISHED'` and orders by `sort_order,id`; use only the published status precedent here.
- Legacy `infra/postgres/study-server/DB.sql` has BIGINT `courses`, `enrollments`, `lessons`, and `lesson_progress`; progress has no declared `(user_id, lesson_id)` uniqueness or percent range check. `infra/postgres/02_study_db.sql` uses an incompatible UUID/V1-PILOT shape and will not be mixed into this endpoint.
- No live database metadata was inspected. Runtime behavior below is a local implementation against the legacy candidate schema, not evidence of deployed schema compatibility.
- Existing worktree is broadly dirty from prior APIs #34 and #47–#64. Preserve all unrelated changes; do not stage, commit, reset, or clean.

## SOURCE_TRACE

- Caller: `apps/study-server/app/api/v1.py` router; add one GET operation and delegate to a new Mentor module.
- Authentication/authorization: `app.utils.auth.validate_current_user_request` validates Bearer/JWT and Mentor role before database access. The existing JWT helper returns numeric user `sub`, used as legacy `courses.mentor_id` in API #62.
- Resource access: query `courses(id, mentor_id)` first. Malformed signed-int64 or missing course maps to catalog 404; an existing course whose `mentor_id` differs from the caller maps to 403. No roster/progress query runs before this check.
- Data source: one read-only aggregate query scoped by `course_id` and `mentor_id`, over distinct active Student enrollments, published lessons, and legacy `lesson_progress`; no mutation, provider call, or #66/#67 dependency.
- Progress duplicate handling: because legacy DDL does not enforce one row per user/lesson, choose one row deterministically with PostgreSQL `DISTINCT ON (user_id, lesson_id)`, latest `last_accessed_at DESC NULLS LAST`, then highest `id DESC`. This is a local DERIVED rule.
- Aggregation: count `COMPLETED` rows only across published lessons; sum selected `progress_percent` values with missing/NULL values as zero; `progress_percent = floor(sum / total published lessons)`, and zero for an empty denominator. A selected row with status outside `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED` or a non-NULL percent outside 0..100 increments `invalid_progress_count`; invalid stored projections produce safe 500. The legacy DDL does not enforce those rules.
- Response: use AC-26's class progress purpose and the existing DD candidate `Page<MentorStudentProgress>` with nested `student`, `completed_lessons`, `total_lessons`, and `progress_percent`. Because catalog #65 directly says `Page<Course>`, this is a visible DIRECT-vs-DERIVED discrepancy, not a catalog rewrite or approval claim.
- Pagination: catalog has no query inputs, so return the entire roster as one page (`page=1`, `size=total=items count`, `total_pages=1` if nonempty, otherwise `size=total=total_pages=0`). This is unbounded and remains a local DERIVED fallback.
- Errors: reuse existing helper and catalog status/business codes. The route reads raw path/header from `Request`, declares OpenAPI parameters and exact 200/401/403/404/500 responses manually, and is in `DESIGN_CONTRACT_PATHS`; no synthetic FastAPI 422 is exposed. Current `error_response` defaults absent error data to JSON `null`, matching the guideline.

## DISCREPANCIES_AND_STATUSES

- `DIRECT`: method/path, Bearer Mentor role, required int64 `course_id`, no query/body, 200 `DESIGN_RESOURCE_RETRIEVED`, and listed 401/403/404/500 error classes.
- `DIRECT/DISCREPANCY`: catalog response is `ApiEnvelope<Page<Course>>`; AC-26 and the DD's purpose require per-Student progress. Implement the DD candidate progress page locally while retaining the catalog contract as the direct source and the DD as Draft.
- `DERIVED`: legacy BIGINT schema mapping, token `sub` to `courses.mentor_id`, 403 for another direct owner, active enrollment and Student role eligibility, published lesson denominator, duplicate progress row selection, completion status, floor-average formula, zero for no lessons, and full-roster one-page metadata.
- `SOURCE_BOUNDARY`: legacy checked-in DDL is candidate schema only; incompatible V1-PILOT schema is excluded; live DB behavior/schema is unverified.
- `CURRENT`: #65 is locally wired and HTTP-tested; #66/#67 remain unwired. #62 roster and #9 curriculum patterns are verified in current source.
- `DISCREPANCY`: Page<Course> direct response has no progress fields; request has no page/size while PageMeta exists. Current error helper emits JSON null when `data` is omitted, matching the guideline.
- `SCOPE`: do not implement #66 learning-event analytics or #67 individual progress, and do not alter shared auth, response, schema, or API catalog.

## IMPLEMENTATION_PLAN

1. DONE — Add strict API #65 progress/page/envelope models and signed-int64 path parser under `app/modules/mentor/api_65_mentor_course_progress/`.
2. DONE — Add SQL constants for direct owner lookup and owner-scoped aggregate over ACTIVE Student roster, PUBLISHED lessons, deterministic latest progress rows and invalid-state counts.
3. DONE — Add Mentor-first view orchestration, 404/403 scope handling, aggregate validation, safe errors and read-only response mapping.
4. DONE — Wire GET route, explicit OpenAPI parameters/responses without synthetic 422, and middleware design-contract path.
5. DONE — Add focused API #65 HTTP tests; linked #62/#9 regressions also pass.
6. DONE — Reconcile all eight DD sheets and reports, preserve direct catalog contract/mismatch, record current local DERIVED behavior, and leave #66/#67 untouched.
7. DONE — Update server-study AGENTS/pages/manifest and this worklog; run full suite, Ruff, OpenAPI, DD static checks, diff check and context validator. The validator's out-of-scope DB Admin baseline finding is recorded below.

## CHANGES

- Runtime: `apps/study-server/app/modules/mentor/api_65_mentor_course_progress/{__init__.py,models.py,query.py,validate.py,view.py}`, route in `app/api/v1.py`, allowlist in `app/core/middleware.py`.
- Tests: `apps/study-server/tests/modules/mentor/api_65_mentor_course_progress/test_mentor_course_progress.py`.
- DD: all eight sheets plus `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, and `VERIFICATION_REPORT.md`; all sheets remain Draft and the template appendices are unchanged.
- CONTEXT_UPDATES: `.agents/context-manifest.json`, server-study AGENTS, declared routes, architecture, runtime, database-security, database, modules and tests pages.
- Assumptions authorized by user conflict-resolution order: use the simplest coherent local behavior supported by AC-26 plus neighboring runtime patterns; explicitly label each noncatalog rule `DERIVED` and preserve the catalog mismatch as `DISCREPANCY`.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog selector/preflight | 58 coding worklogs available; selected three and read all three. | `VERIFIED_PREFLIGHT` |
| Current source and conflict review | #62 access/roster, #9 published lessons, auth/middleware/router patterns, legacy DDL, AC-26 and #65 DD reviewed. | `VERIFIED_SOURCE_REVIEW` |
| API #65 focused HTTP tests | `uv run pytest -q tests/modules/mentor/api_65_mentor_course_progress` — 20 passed; one upstream TestClient deprecation warning. | `VERIFIED_LOCAL_HTTP` |
| Linked regression tests | APIs #65/#62/#9 — 47 passed; one upstream warning. | `VERIFIED_LOCAL_HTTP` |
| Full Study suite | `uv run pytest -q` — 680 passed; one upstream TestClient deprecation warning. | `VERIFIED_LOCAL_SUITE` |
| Ruff | `uv run ruff check app tests` — all checks passed. | `VERIFIED_STATIC` |
| OpenAPI/import | 35 `/api/v1` path templates, 36 `/api/v1` operations; API #65 exact 200/401/403/404/500, int64 path, required Authorization header, no request body/query or 422. | `VERIFIED_STATIC` |
| DD Markdown | 8/8 template appendices byte-identical to source; local links, JSON, fences and whitespace pass. | `VERIFIED_STATIC` |
| `git diff --check` | No whitespace diagnostics. | `VERIFIED_STATIC` |
| Context validator | `deno run --allow-read --allow-env --allow-run scripts/validate-agent-context.mjs --skip-drift` reports only missing `.agents/db-admin/**` pages and `apps/db-admin-*` source roots/links; no Study Server context errors. Node is unavailable in this environment. | `BASELINE_FAILURE_OUTSIDE_SCOPE` |

## HANDOFF

- Remaining limits: Catalog response mismatch and unbounded page need owner decision; checked-in legacy DDL/fake DB tests do not prove live schema/deployment or business approval. Global context validation remains invalid because the DB Admin scope is absent from this checkout.
- Next owner/action: Continue the authorized API sequence with API #66; preserve existing dirty changes and keep local verification distinct from deployment evidence.
