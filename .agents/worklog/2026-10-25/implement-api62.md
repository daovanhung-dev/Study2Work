---
task_id: "2026-10-25-implement-api62"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #62

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 55 available; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve shared JWT/role guards, purpose-bound UploadAsset scope and DB/object-storage verification boundaries.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Keep `query.py` SQL-only; caller owns transactions; reuse direct course owner and ordered UploadAsset patterns where API contract supports them.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Trace linked APIs and physical relations before choosing response projection; preserve dirty worktree and distinguish checked-in DDL from live schema.
- shortage: `none`
- related_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api49-mentor-content-list.md`
    - carry_forward: Closest list-cardinality precedent; a singular Page<Course> catalog response was changed to a plain array when workflow semantics and absent page/size inputs required it; catalog/diagram were synchronized and Draft status retained.

## EXPECTED_BEHAVIOR

- Requirement: Implement API #62 `GET /api/v1/mentor/courses/{course_id}/students` for the AC-25 recipient picker; this task remains scoped to Study Server API #62.
- Canonical inputs/errors: Bearer JWT Mentor; `course_id:int64!`; no query/body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; catalog errors 401/403/404/500.
- Diagram flow: read active enrollments, then allow Mentor to select recipients; API #63 creates/dispatches notifications and API #64 reads delivery status.
- User direction: Resolve source conflicts with the requested source precedence and use the simplest coherent fallback without inventing a Course-shaped roster or pagination inputs.
- Selected fallback, `DERIVED — Draft — Needs Confirmation`: return `ApiEnvelope<UserSummary[]>`, with one row per eligible Student and no pagination because #62 has no page/size request parameters. Synchronize the API catalog and AC-25 API node so the executable design contract matches the roster use case.
- Persistence/eligibility fallback, `DERIVED`: use checked-in legacy BIGINT `courses`, `enrollments` and `users`; select `enrollments.status = 'ACTIVE'` and `users.role = 'STUDENT'`; return distinct Student IDs ordered ascending. V1-PILOT UUID tables/statuses are not mixed into this API.
- Authorization fallback, `DERIVED`: require current Study Mentor JWT guard and direct ownership `courses.mentor_id = authenticated numeric subject`, matching existing Mentor APIs #46/#49/#54. Missing course→404; existing course owned by another Mentor→403; an empty roster→200 with `data: []`.
- API #63’s `recipients:string!` encoding remains an integration question; #62 returns numeric UserSummary IDs and does not invent a serialization format for #63.

## CURRENT_BEHAVIOR

- Pre-edit source baseline: no API #62 route/module/test existed; API #61 was the last wired Mentor route and `DESIGN_CONTRACT_PATHS` lacked #62.
- Final source: #62 route/module/query/models/path validator and TestClient suite are wired. It uses the shared MENTOR guard, numeric JWT subject, direct `courses.mentor_id`, raw signed-int64 path handling, distinct `ACTIVE` enrollment rows joined to Student users, and `UserSummary[]` with no pagination.
- Error/side-effect behavior: malformed/out-of-range or missing course→404; role/owner mismatch→403; query/projection failure→500; empty roster→200 `[]`; read-only, no commit. The path is in `DESIGN_CONTRACT_PATHS`.
- Persistence source: legacy DDL defines BIGSERIAL courses, nullable BIGINT enrollment references, `status VARCHAR DEFAULT 'ACTIVE'`, and users; API #34 also checks `ACTIVE`. V1-PILOT uses UUID versioned enrollments and `ENROLLED|IN_PROGRESS|COMPLETED`; it remains separate.
- Runnable tests: API #62 focused suite passes 18 tests; linked #49/#54 regression passes 32 tests; final full Study suite passes 615 tests.
- Runtime/deployment: source and local DDL are checked-in evidence only; no live DB/deployment access was performed.

## SOURCE_TRACE

```text
GET /api/v1/mentor/courses/{course_id}/students
  -> FastAPI raw path/OpenAPI int64 -> shared validate_current_user_request(role="MENTOR")
  -> numeric principal -> signed-int64 parse
  -> SELECT courses.id/mentor_id -> 404 missing / 403 owner mismatch
  -> SELECT DISTINCT users.id/full_name/avatar_url through ACTIVE enrollments, scoped to course and Mentor
  -> ApiEnvelope<UserSummary[]> / 401 / 403 / 404 / 500
  -> read-only; no commit and no notification side effect (#63 owns dispatch)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Roster cardinality and payload | AC-25 selects recipients after reading active enrollments; diagram/catalog currently repeat `Page<Course>`, which cannot represent a student roster. API #49 is an implemented precedent for resolving a list-purpose/singular-payload conflict. | `RESOLVED_BY_DERIVED_FALLBACK` | Use `UserSummary[]`, no PageMeta, no Course-shaped fabricated entries; keep DD Draft and synchronize catalog/diagram. |
| Pagination | Request has only `course_id`; there is no page/size input. | `RESOLVED_BY_DERIVED_FALLBACK` | Return the full distinct roster as a plain array; do not add an unusable fixed page or new request fields. |
| Legacy vs V1-PILOT enrollment schema | `DB.sql` and API #34 support BIGINT/ACTIVE; V1-PILOT uses UUID/versioned course enrollment and different statuses. Live schema is not queried. | `RESOLVED_BY_DERIVED_FALLBACK` | Query the legacy table family only; document that checked-in DDL does not prove live deployment. |
| Active recipient eligibility and duplicate rows | Diagram says active enrollments; legacy status default is ACTIVE; legacy DDL lacks `(course_id,user_id)` uniqueness. | `RESOLVED_BY_DERIVED_FALLBACK` | Filter exact `ACTIVE`, require Student role, use `DISTINCT`, stable `users.id ASC`; no extra account-status filter. |
| Mentor scope and missing/empty behavior | #46/#49/#54 use numeric Mentor subject and direct `courses.mentor_id`; catalog lists 403/404; endpoint is a recipient collection. | `RESOLVED_BY_DERIVED_FALLBACK` | Use direct-owner scope, missing course 404, other owner 403, empty roster 200 `[]`. Assigned-course access remains unsupported. |
| API #63 recipient encoding | #63 declares `recipients:string!` but no serializer/ID format is declared. | `OPEN — LINKED API CONTRACT` | #62 exposes numeric IDs; leave CSV/JSON/other encoding to API #63 design; do not implement or change #63. |
| Live DB schema/deployment | Only checked-in DDL/migrations/source are available. | `NOT_VERIFIED_HERE` | Do not report live behavior as verified. |

## IMPLEMENTATION_PLAN

1. Use AC-25 activity semantics first: Mentor reads active enrollments, selects recipients, then #63 sends and #64 reports; record its internal `Page<Course>` output contradiction instead of treating a Course row as a learner.
2. Use current Study infra second: legacy BIGINT `courses/enrollments/users` and API #34's exact `ACTIVE` predicate are the runtime-facing local candidate; keep V1-PILOT UUID/versioned enrollment isolated and state live DDL is unverified.
3. Use catalog third, then apply the authorized simple fallback: change #62 success payload to `UserSummary[]`; keep `course_id` as the only input; do not add pagination or choose #63's string encoding.
4. Before runtime edits, update the existing API #62 DD sheets/reports, catalog row and AC-25 diagram node to record `DERIVED — Draft — Needs Confirmation`, direct-owner access, recipient filters, distinct ordering, missing/empty behavior and unresolved #63 encoding. Preserve all template source appendices.
5. Implement only API #62 in a thin router + API module: shared Mentor guard; signed-int64 raw path parser; course existence/owner check; SQL-only distinct active Student query scoped to Mentor; strict UserSummary mapping; standard 401/403/404/500 envelope; no write/commit.
6. Add TestClient coverage for success/empty/dedup ordering, auth/role, malformed/out-of-range and missing ID, owner mismatch before roster query, DB/projection errors, trace envelope and OpenAPI int64/array schema.
7. Review #63/#64 contract boundary and #49/#54 implementation precedent without changing linked API behavior. Update server-study route/module/database/test context and manifest.
8. Run focused #62 tests, linked #49/#54 regression tests, full Study suite, Ruff, OpenAPI/import checks, DD link/JSON checks, `git diff --check`, and context validation; preserve the dirty worktree and report live DB/deployment limitations.

## CHANGES

- Runtime: added `apps/study-server/app/modules/mentor/api_62_mentor_course_students/{__init__,models,query,validate,view}.py`; wired the thin API #62 route in `app/api/v1.py` and registered its contract path in `app/core/middleware.py`.
- Tests: added `apps/study-server/tests/modules/mentor/api_62_mentor_course_students/test_mentor_course_students.py` with auth/scope, active Student projection, empty, path, error, trace, read-only and OpenAPI cases.
- Contract/DD: changed API #62 catalog and AC-25 diagram output to `ApiEnvelope<UserSummary[]>`; updated the 8 API #62 sheets, `OPEN_QUESTIONS.md`, `PLAN_RESULT.md` and `VERIFICATION_REPORT.md`; preserved all Excel source appendices.
- Context: updated `.agents/server-study/{AGENTS,architecture,apis/declared-routes,core/database-security,core/runtime,database,modules/README,tests}.md` and `.agents/context-manifest.json`.
- Schema: no DDL or migration change; implementation reads existing checked-in legacy tables only.
- Boundary: API #63/#64 behavior is unchanged; #63 recipient string encoding stays open. Existing unrelated dirty worktree changes were preserved; no cleanup, staging or commit was done.
- Assumptions: `UserSummary[]` with no pagination, legacy BIGINT schema, `ACTIVE`+`STUDENT` eligibility, direct course ownership and empty-array success remain DERIVED and need owner confirmation. Live DB/deployment was not verified.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 55 available; selected three same-type worklogs and read each. | `VERIFIED_PREFLIGHT` |
| API #62 focused TestClient | 18 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Linked #49/#54 TestClient regression | 32 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Full Study suite `uv run pytest -q` | 615 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| `uv run ruff check app tests` | All checks passed. | `PASS` |
| OpenAPI/import | 32 API v1 path templates, 33 operations; #62 uses int64 path metadata and array response schema. | `PASS` |
| DD static validation | 11 files, JSON examples valid, local links resolve, AC-03 Draw.io XML parses. | `PASS` |
| `git diff --check` | No whitespace errors. | `PASS` |
| Context validator full / `--skip-drift` | Full: broad dirty-source drift plus missing DB Admin pages/source. `--skip-drift`: unrelated missing DB Admin context/source only; no Study Server page/reference error. | `FAILED — BASELINE` |
| Live DB/schema/deployment | Not accessed. | `NOT_VERIFIED_HERE` |

## HANDOFF

- API #62 implementation and local verification are complete. DERIVED response/schema/authorization decisions remain `Draft — Needs Confirmation`; API #63 recipient encoding and live schema/deployment remain open.
- Next task in the one-API-per-session sequence: API #63. Preserve the shared dirty worktree and run a fresh coding-worklog preflight for that session.
