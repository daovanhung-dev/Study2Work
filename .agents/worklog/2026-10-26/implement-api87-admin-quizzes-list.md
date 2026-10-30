---
task_id: "2026-10-26-implement-api87-admin-quizzes-list"
date: "2026-10-26"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "COMPLETED"
---

# Worklog: Implement Study Server API #87 Admin quiz list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 80 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-26/implement-api74-admin-course-detail.md`
    - carry_forward: Shared ADMIN auth before raw input parsing; use legacy BIGINT only as a candidate; preserve the dirty worktree and mark unresolved semantics DERIVED.
  - path: `.agents/worklog/2026-10-26/implement-api75-admin-course-update.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns DB execution and transaction behavior; retain scope-specific fallback decisions and do not stage/commit.
  - path: `.agents/worklog/2026-10-26/implement-api76-admin-course-status.md`
    - carry_forward: AC-35/32 relationship decisions must not be inferred from AC-32; checked-in migrations and fake-session tests are not live-schema evidence.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: implement `GET /api/v1/admin/quizzes` for AC-35/API #87.
- Direct contract from AC-35 and API catalog row #87: Admin Bearer JWT; optional `course:int64`, `status:string`, `page:int32`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; `ApiEnvelope<Quiz>`; exact declared errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-35 says Admin has quiz-management permission, then opens quiz management, queries quizzes, and chooses Create/Update/Delete/Statistics. The diagram does not define page size/order, list response cardinality, nested question inclusion, or permission claim mapping.

## CURRENT_BEHAVIOR (pre-edit)

- API #87 route, module, and tests are absent. Current API count is 50 `/api/v1` path templates / 57 operations; APIs #68–#86 are wired. The current middleware `DESIGN_CONTRACT_PATHS` does not include `/api/v1/admin/quizzes`.
- Existing Admin list patterns: #78 returns `Page<Content>` with count/page predicates, fixed size 20 and `id ASC`; #82 returns unpaginated `Lesson[]`; public #07 uses `page=1`, fixed size 20, stable ordering, count/page query pairing, and a `Page<T>` response. These are implementation precedents, not API #87 direct contract.
- Shared `validate_current_user_request(..., role="ADMIN")` is current Admin auth. AC-35's finer quiz-management permission has no source-backed claim/policy.
- Legacy `infra/postgres/study-server/DB.sql` defines BIGINT `quizzes`, `quiz_questions`, `quiz_choices`, attempts and answers. `quizzes.course_id` and `passing_score` are nullable; `quiz_questions` has no question type; `quiz_choices` has no choice order. V1-PILOT uses UUID `assessments`/questions/options and is not compatible with this int64 API contract. Neither artifact proves the live schema.
- Catalog `Quiz` requires `questions:QuizQuestion[]`; `QuizQuestion` requires `type:QuestionType` and `choices:QuizChoice[]`, but neither QuestionType values nor QuizChoice schema is defined. The legacy DDL cannot faithfully supply these nested fields.
- Re-review of API #28 Response/Data Mapping and API #88 Data Mapping confirmed the same gaps: #28 uses an empty-list example without claiming the source Quiz has no questions; #88 confirms legacy BIGINT persistence has no question type and QuizChoice output fields/order remain SOURCE_REQUIRED. The UUID pilot model does not repair the BIGINT mapping. Keep `questions=[]` as an explicitly unloaded local fallback instead of returning a malformed partial nested object.
- Worktree already contains 555 modified/untracked entries across Study source, DD, schema and context. Preserve them; do not stage, commit or clean.

## SOURCE_TRACE

```text
GET /api/v1/admin/quizzes
  -> route passes raw query/header so shared ADMIN guard runs first
  -> validate signed-int64 course and positive signed-int32 page; exact status string
  -> count + fixed-size 20-page query over legacy BIGINT quizzes
  -> exact optional filters; always hide status='DELETED' by AC-35/#90 list policy
  -> map Quiz metadata; use questions=[] because list diagram has no nested-read step and the source cannot define QuestionType/QuizChoice
  -> build Page<Quiz>, return success envelope without commit; safe query/projection failures rollback and return DESIGN_INTERNAL_ERROR
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response cardinality | Catalog and diagram say `ApiEnvelope<Quiz>`; endpoint/list intent and `page` imply a collection. | `DISCREPANCY / DERIVED` | Use `ApiEnvelope<Page<Quiz>>`, following reusable Page and #07/#78 pagination precedents; retain Draft/open owner decision. |
| Nested question projection | Quiz requires questions/type/choices; AC-35 only queries quizzes; legacy question has no type and QuizChoice is undefined. | `DISCREPANCY / DERIVED` | Return metadata-only list entries with `questions=[]`; do not invent nested fields or map pilot UUID types. Record prominently in DD. |
| Page behavior | `page` is direct; size/order/count are not specified. #07/#78 use page 1, fixed size 20 and stable order. | `DERIVED` | Default page 1, fixed size 20, `id ASC`, count/page filters identical. |
| Deleted visibility | API #90 DD proposes `status='DELETED'` tombstone and default hiding in #87; status is not yet canonical. | `DERIVED` | Exclude tombstones unconditionally, including when an explicit `status=DELETED` filter is sent, consistent with Admin #82. |
| Admin permission | AC-35 requires quiz-management permission; current helper supports shared ADMIN role only. | `SOURCE_REQUIRED / DERIVED` | Enforce role ADMIN; do not claim fine-grained permission is implemented. |
| Query parse errors | Catalog lists only 401/403/500; current FastAPI validation convention and Admin #78 map invalid filters to 422. | `DISCREPANCY / DERIVED` | Return 422 `DESIGN_VALIDATION_ERROR` for malformed/out-of-range course/page to avoid silently broadening a query. Document the additional local error behavior; do not alter catalog. |
| Nullable source fields | Legacy DDL permits NULL course_id/passing_score but Quiz requires both. | `DISCREPANCY` | Fail safe with 500 on an invalid required row projection; do not substitute values or silently omit rows. |
| Live database | Checked-in legacy DDL and fake-session tests only. | `UNVERIFIED` | No claim about live schema, migrations, SQL execution or deployment. |

## IMPLEMENTATION_PLAN (PRE-CODE)

1. Complete source-order review: AC-35 index/activity diagram → legacy DDL, DB table guide/ERD and V1-PILOT comparison → exact catalog row/reusable schemas. Trace current API #07, #78, #82, #86, shared ADMIN auth, response helpers, middleware and matching tests; inspect #90 tombstone proposal for AC-35 consistency.
2. Keep API #87 DD `Draft — Needs Confirmation`; record the decision and this plan before editing implementation source. Preserve all unrelated worktree changes.
3. Add `admin/api_87_admin_quizzes_list/models.py` with declarative query/Page/Quiz/envelope classes only; do not define invented `QuestionType` or `QuizChoice` members. Represent nested questions as an empty list in the local list projection.
4. Add SQL-only constants for a count and a page query against legacy `quizzes`; use identical optional `course_id`/`status` predicates, exclude `DELETED` unconditionally, order by `id ASC`, and bind `limit`/`offset`.
5. Add `validate.py`: call shared ADMIN guard before input parsing; parse `course` as signed int64 and `page` as signed int32 with positive page bounds/default 1; preserve status exactly; map invalid input to a field-specific 422 `DESIGN_VALIDATION_ERROR`.
6. Implement `view.py`: execute count and list with the same filters, validate count/page shape, map strict required Quiz metadata (legacy `name`→`title`, `time_limit_minutes`→`duration_minutes`, `passing_score`→decimal string), create Page metadata (fixed size 20), omit nested reads by returning `questions=[]`, rollback on SQL/mapping errors, and never commit on GET.
7. Wire GET `/admin/quizzes` in `app/api/v1.py` using raw query inputs, int64/int32 OpenAPI parameter schemas, Authorization header, 200/401/403/422/500 responses and no body. Add the exact route to `DESIGN_CONTRACT_PATHS` so errors use DESIGN codes.
8. Add focused HTTP tests for Admin/auth-first behavior; query parsing and exact filters; pagination/count consistency; DELETED hiding; empty/out-of-range pages; required metadata/decimal mapping; malformed count/rows; SQL failure/rollback/no-commit; trace/envelope and OpenAPI.
9. Load/apply registered `createDD-markdown` before DD edits. Update API #87's sheets/reports/open questions with the implemented DERIVED choices and current source/tests while retaining the direct contract, template appendix bytes and Draft status; do not edit catalog, diagrams or schema.
10. Update only directly affected `.agents/server-study` context, `.agents/project/source-status.md`, `.agents/context-manifest.json`, and this worklog with route/module/test/count/status evidence. Record live schema, permission, response/nested-shape and catalog error gaps.
11. Verify API #87 focused tests, linked #07/#78/#82/#86 regressions, full Study suite, Ruff, import/OpenAPI, SQL/predicate consistency, DD/template/link/JSON checks, `git diff --check`, and context validator using the available Deno fallback if Node is absent. Separate unrelated DB Admin baseline validator findings.
12. Review only the API #87 and directly linked context/DD diff; preserve the existing dirty worktree and do not stage or commit.

## CHANGES

- Added and wired API #87 GET route, Admin module, query validation, count/page SQL, metadata response mapping, safe errors, rollback behavior and middleware allowlist entry.
- Added 20 focused HTTP tests using fake DB sessions, covering auth-first ordering, query parsing/filtering, pagination, tombstone exclusion, mapping/error cases, trace/envelope and OpenAPI.
- Updated all 11 Markdown files in `apps/study-server/docs/dd/87_admin_quizzes_list/`; kept `Draft — Needs Confirmation`, direct catalog type/error set, template appendices and unresolved contract/schema gaps.
- Updated Study context and project source-status for 51 route templates / 58 operations and 1113 passing tests; registered API #87 module/test source paths in `.agents/context-manifest.json`.
- Preserved the shared dirty worktree; no staging, commit, cleanup, catalog, diagram or database-schema change.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Deno selector selected and all three `coding` worklogs listed above were read; no shortage. | `VERIFIED_PREFLIGHT` |
| API #87 focused tests | `.venv/bin/pytest -q tests/modules/admin/api_87_admin_quizzes_list/test_admin_quizzes_list.py` | `PASS: 20` |
| Linked #07/#78/#82/#86/#87 regression | Focused test files for APIs #07, #78, #82, #86, #87 | `PASS: 93` |
| Full Study suite | `.venv/bin/pytest -q` | `PASS: 1113; 1 upstream Starlette/httpx deprecation warning` |
| Ruff | `.venv/bin/ruff check app tests` | `PASS` after formatting three new test lines |
| OpenAPI | Import `app.main`, count `/api/v1` templates/operations and #87 statuses | `PASS: 51 / 58; #87 200/401/403/422/500` |
| DD static/template/link/JSON | 11 files; appendix parity 8/8; 35 local links; JSON examples, fences and newline checks pass. | `PASS` |
| `git diff --check` | Repository diff whitespace check | `PASS` |
| Context validator | Full Deno run reports pre-existing missing `db-admin` pages/sources and source drift against baseline; `--skip-drift` leaves only the same unrelated `db-admin` graph/source errors. No API #87 registered path is missing. | `PARTIAL — unrelated baseline blocker` |

## CONTEXT_UPDATES

- `.agents/server-study/AGENTS.md`, `architecture.md`, `apis/declared-routes.md`, `core/runtime.md`, `core/database-security.md`, `database.md`, `modules/README.md`, `tests.md`, `workflows/README.md`: API #87 local runtime and verification boundary.
- `.agents/project/source-status.md`: current route/test counts and API #87 status.
- `.agents/context-manifest.json`: registered five API #87 module files and focused test file.

## HANDOFF

- Remaining limits: live schema/permissions and the canonical collection/nested Quiz contract are not established by local artifacts.
- Next owner/action: start API #88 in a separate session; keep API #87 list/Page cardinality, nested Quiz schema, live database and fine-grained permission open until authoritative evidence is available.
