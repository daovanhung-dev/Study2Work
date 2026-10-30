---
task_id: "2026-10-26-implement-api91-admin-quizzes-statistics"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #91 Admin quiz statistics

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 84 available; selected three; shortage none.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN auth before raw path parsing; preserve the dirty worktree; DDL and fake DB tests do not prove live DB state.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns DB orchestration and response mapping.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: Do not infer a fine-grained permission from the shared ADMIN role; keep derived rules explicit and DD Draft.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

Within-scope dependencies are AC-35 APIs #87–#90 and AC-16 APIs #29–#32. They do not cross application scopes.

## EXPECTED_BEHAVIOR

- Follow user priority: AC diagram → infrastructure/schema → API catalog → simplest explicit fallback when the sources remain in conflict.
- AC-35 shows Admin selecting STATISTICS, invoking `GET /api/v1/admin/quizzes/{quiz_id}/statistics`, then aggregating attempt statistics. It gives no metric names or output fields.
- Catalog #91 requires Admin Bearer JWT and `quiz_id:int64!`, no body/query, HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Quiz>`, and exactly 401/403/404/500 with the listed `DESIGN_*` codes.
- API #91 DD remains `Draft — Needs Confirmation`. It separates the direct catalog `Quiz` response from a `DERIVED` `QuizStatistics` proposal. Implement the smallest statistics DTO recorded in that proposal, with the catalog conflict and owner decisions still explicit; do not add fields to reusable `Quiz` or change catalog/diagram/schema.
- Candidate metrics per DD: all linked attempts; submitted when `submitted_at IS NOT NULL`; graded when `score IS NOT NULL`; average over non-NULL scores; passed at `score >= passing_score`; percent is passed / graded × 100. No status filter, answer join, per-user data, or date/pagination filter.
- A NULL passing threshold yields NULL passed count/rate; no scored attempts yields NULL average/rate. A retained quiz tombstone remains readable for history; no parent row returns catalog 404. These are DERIVED.

## CURRENT_BEHAVIOR (pre-edit)

- Current route chain in `app/api/v1.py` wires Admin quiz APIs #87–#90; #91 module, endpoint, and tests are absent. The existing `/api/v1/admin/quizzes/{quiz_id}` middleware template does not match the `/statistics` suffix, so #91 needs its own allowlist entry.
- `validate_current_user_request(..., role="ADMIN")` is the shared source-backed guard. AC-35 quiz-management permission has no dedicated policy/claim mapping.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` states aggregate attempt statistics but its #91 output is `ApiEnvelope<Quiz>` and defines no metric fields. Catalog row #91 independently also says `ApiEnvelope<Quiz>`.
- `infra/postgres/study-server/DB.sql` is a checked-in legacy BIGINT candidate: `quizzes(id, passing_score, status)` and `quiz_attempts(id, quiz_id, submitted_at, score, status)`. It allows nullable `passing_score` and `quiz_id`. V1-PILOT `infra/postgres/02_study_db.sql` uses UUID assessments/attempts and is a separate model. Live schema/deployment is not verified.
- AC-16 diagram and DD #29–#32 use IN_PROGRESS, PENDING_GRADE, and GRADED in portions of the attempt lifecycle; this is not a complete status enum. No attempt lifecycle implementation exists to depend on.
- Existing worktree has 857 changed/untracked entries. Preserve all, including pre-existing changes in API #91 DD `02_Overview.md`, `06_Error.md`, and `OPEN_QUESTIONS.md`; do not clean, stage, or commit.

## SOURCE_TRACE

```text
raw GET route -> shared ADMIN JWT guard -> parse raw positive signed-int64 quiz_id ->
one parameterized aggregate query over legacy quizzes LEFT JOIN quiz_attempts ->
validate count/decimal/identity projection -> QuizStatistics envelope -> HTTP response
```

The read is non-mutating. Query, mapping, and serialization failures return safe 500 with read-transaction rollback; missing parent and malformed/overflow IDs return the exact catalog 404. No quiz_answers or Student identifiers are read or returned.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Statistics purpose vs response | Diagram says aggregate statistics; diagram/catalog return `ApiEnvelope<Quiz>` whose schema has no metrics. | `DISCREPANCY` | Keep direct contract visible; implement separately named `QuizStatistics` only as the DD's DERIVED fallback; leave questions open and DD Draft. |
| Metric definitions and threshold | Diagram/catalog define no metrics; DD proposes count/null/threshold rules. | `DERIVED` | Implement proposal exactly, with no status or answer filtering; retain owner questions. |
| Deleted/history visibility | #90 DD preserves history on quiz tombstone; #91 DD proposes aggregate while row exists. | `DERIVED` | Do not filter quiz status; absent row is 404. |
| Admin permission | Catalog/AC-35 call for Admin quiz-management permission; source has shared ADMIN role only. | `SOURCE_REQUIRED` | Use shared ADMIN guard before parsing and DB; do not claim dedicated permission enforcement. |
| Active schema | Legacy BIGINT DDL and UUID V1-PILOT artifacts differ; no live metadata. | `NOT_VERIFIED` | Query legacy BIGINT candidate only; make no deployment claim. |
| Path parse failure | Direct #91 errors exclude 422; int64 min/positivity details are unspecified. | `DERIVED` | Positive signed-int64 parse; malformed/out-of-range -> direct 404 to preserve exact error set. |
| Decimal rounding | DDL is numeric; DD says decimal-string and leaves scale/rounding open. | `SOURCE_REQUIRED` | Return finite non-exponent decimal string without application rounding; preserve source numeric scale where the driver supplies it. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete targeted source review: exact #91 diagram/catalog/schema, attempt lifecycle, current route/middleware/auth/response helpers, linked #87/#89/#90 patterns and tests. Keep direct, runtime, and DERIVED evidence distinct.
2. Record this source trace and plan before runtime/DD/context changes; retain all pre-existing worktree edits.
3. Add `app/modules/admin/api_91_admin_quizzes_statistics/` with strict response/envelope models, one SQL-only aggregate query, ADMIN/raw-path validation, and read-only view orchestration. Keep query SQL in `query.py` and all execution/rollback/projection logic in `view.py`.
4. Query one parent quiz with a LEFT JOIN to attempts and aggregate COUNT/AVG/FILTER expressions. Do not filter tombstone or attempt status; do not join answers. Validate parent identity, int64 counts, count relationships, nullable metrics, finite decimal values and 0–100 pass rate before success.
5. Wire GET `/admin/quizzes/{quiz_id}/statistics` using raw path capture so ADMIN auth runs before path parsing. Declare only 401/403/404/500 and exact OpenAPI int64 path/auth metadata. Add the exact route template to `DESIGN_CONTRACT_PATHS`.
6. Add focused HTTP/OpenAPI tests for ADMIN-before-parse/DB, malformed and overflow path, zero attempts, submitted/ungraded and graded attempts, NULL threshold, pass calculations, no tombstone filter, absent quiz, safe query/projection errors, rollback/read-only behavior, response/trace and route precedence.
7. Update API #91 DD sheets/reports in place to distinguish intended direct schema from implemented DERIVED DTO, record source-backed current behavior/test results, and retain `Draft — Needs Confirmation` and open owner questions. Preserve all template appendix tails and existing user edits.
8. Update only the connected Study context pages, source-status registry and context manifest for API #91. Recount current route/operation/test totals rather than carrying forward historical totals.
9. Run focused and full Study tests, scoped/full Ruff checks, OpenAPI route/error checks, DD static checks, `git diff --check`, and the Deno context validator. Report fake DB vs live-schema/deployment boundary and unrelated validator findings.
10. Review the scoped diff and final Git status; do not stage or commit.

## PRE-CODE CHECKPOINT

- Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, selector output and all three selected coding worklogs were loaded; shortage none.
- Read `.agents/server-study/AGENTS.md`, `INDEX.md`, `apis/declared-routes.md`, `core/database-security.md`, `tests.md`, and the worklog README/template. The manifest wires `createDD-markdown`; its DD workflow was read earlier in this task.
- Inspected the AC-35 diagram, catalog row/schema, legacy and V1-PILOT DDL, AC-16/API #29–#32 DD lifecycle, API #87/#89/#90 source patterns, current route composition and `DESIGN_CONTRACT_PATHS`.
- Confirmed route/module/test are absent and captured the pre-existing 857-entry dirty worktree. No API #91 runtime, DD, or context edit has been made at this checkpoint.

## CHANGES

- Runtime: added `admin/api_91_admin_quizzes_statistics/` with strict `QuizStatistics` fallback/envelope models, int64 OpenAPI fields, SQL-only aggregate, shared ADMIN/raw-path validator, and read-only query/mapping view. Wired GET in `app/api/v1.py` and added the exact statistics path to `DESIGN_CONTRACT_PATHS`.
- Tests: added focused HTTP/OpenAPI coverage for auth order, path bounds, zero/submitted/ungraded/graded/null-threshold metrics, missing quiz, invalid projections, safe query failure, rollback/read-only behavior, trace and exact catalog error set.
- DD: updated the API #91 package and reports with current local wiring/results. Kept direct `ApiEnvelope<Quiz>` visible as a diagram/catalog conflict, the implementation `QuizStatistics` DTO and metric/path rules DERIVED, all owner questions open, and status `Draft — Needs Confirmation`.
- Context: updated the Study route, runtime, architecture, database/security, module/test/workflow pages, project source status and context manifest for #91; API #29–#32 and #92–#103 remain accurately marked unwired.
- No schema, migration, catalog or diagram changes. Preserved pre-existing DD edits and the rest of the dirty worktree; no staging or commit.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Coding worklog selector | 84 available; selected #74–#76; all three read; shortage none. | `VERIFIED_PREFLIGHT` |
| Focused API #91 suite | `.venv/bin/pytest tests/modules/admin/api_91_admin_quizzes_statistics/test_admin_quizzes_statistics.py -q` — 19 passed; one upstream Starlette/httpx TestClient warning. | `VERIFIED_LOCAL_HTTP` |
| Linked #87–#91 regression | `.venv/bin/pytest tests/modules/admin/api_87_admin_quizzes_list tests/modules/admin/api_88_admin_quizzes_create tests/modules/admin/api_89_admin_quizzes_update tests/modules/admin/api_90_admin_quizzes_delete tests/modules/admin/api_91_admin_quizzes_statistics -q` — 104 passed; one upstream warning. | `VERIFIED_LOCAL_HTTP` |
| Full Study suite | `.venv/bin/pytest -q` — 1197 passed; one upstream Starlette/httpx TestClient deprecation warning. | `VERIFIED_LOCAL_HTTP` |
| Ruff | `.venv/bin/ruff check app tests` passed; scoped `ruff format --check` passed for 8 changed source/test/router files. | `VERIFIED_SCOPED` |
| OpenAPI | 53 `/api/v1` path templates / 62 operations; #91 has exact 200/401/403/404/500, int64 path/counts, Authorization, no body/query. | `VERIFIED_LOCAL_SCHEMA` |
| DD package | 11 files; 8/8 template appendix tails preserved; 5 JSON examples parse; 28 relative link targets exist. | `VERIFIED_STATIC` |
| Context manifest/validator | Manifest JSON and all six new source paths validate. Deno validator reports only pre-existing missing DB Admin pages/source roots/links; no server-study/API91 finding. | `VERIFIED_STUDY_SCOPE; UNRELATED_DB_ADMIN_FINDINGS` |
| Diff hygiene | `git diff --check` passes. Fake DB tests do not verify live PostgreSQL/schema/deployment. | `VERIFIED_LOCAL` |

## HANDOFF

- Remaining blockers: Owner decisions remain open for response schema, metric policy/rounding, threshold NULL, tombstone visibility, fine-grained Admin permission, and live schema.
- Next owner/action: Continue the active API sequence with #92. Do not treat the local DERIVED fallback as owner approval or live DB verification.
