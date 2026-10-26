# Báo cáo kiểm tra — API #74

Trạng thái: local source/test verification completed on 2026-10-26. The DD remains `Draft — Needs Confirmation`; no live database or deployment was verified.

## Evidence reviewed

| Source | Result |
|---|---|
| AC-32 activity diagram | `#73 → #74 course/owner/counters → #75/#76/#77 → reload`; counters have no response field definition. |
| Legacy and V1-PILOT DDL | Legacy `courses/users` use BIGINT and fit the API int64 candidate; V1-PILOT UUID/versioned model is incompatible. Neither verifies live schema. |
| API catalog and reusable schemas | Direct route/auth/`ApiEnvelope<Page<Course>>`/200 and 401/403/404/500 retained. Course lacks counters; category is optional. |
| Current #08/#69/#73 and shared auth/mapping/middleware | Public detail is a singleton Page precedent; Admin detail uses shared role guard, safe Course mapper and route-template middleware matching. |

## Verification

| Check | Result |
|---|---|
| Focused API #74 suite | `15 passed`, one upstream Starlette/httpx deprecation warning. |
| Linked #06/#08/#69/#73/#74 regression | `80 passed`, same warning. |
| Full Study Server suite | `845 passed`, same warning. |
| Ruff | `.venv/bin/ruff check app tests` — all checks passed. |
| OpenAPI | Route exists as `GET /api/v1/admin/courses/{course_id}` with signed-int64 path metadata and catalog 401/403/404/500 errors; overall 42 unique `/api/v1` templates / 45 operations. |
| Error/middleware | Dynamic route template is in `DESIGN_CONTRACT_PATHS`; middleware resolves FastAPI route template; current error helper defaults `data:null`. |
| Agent context validator | Deno fallback with `--skip-drift` still reports missing DB Admin context/source roots and broken DB Admin links outside this scope. | `BASELINE_FAIL_OUT_OF_SCOPE` |
| DD appendices / diff | All 8 template appendix suffixes match the prior file byte-for-byte; `git diff --check` passes. | PASS |
| Worktree/static boundaries | No migration or catalog/diagram edit for #74; all other dirty worktree files were preserved. |

## Implemented local fallbacks

- Shared JWT role `ADMIN` is enforced before path parsing/DB access; dedicated course-management permission policy remains absent.
- One bound legacy BIGINT candidate read uses `courses LEFT JOIN users`, does not filter status, and does not query category/counters.
- Response is one mapped `Course` in `Page<Course>` with page metadata 1/1/1/1; invalid/out-of-int64 path maps to 404.
- Query/projection errors map to safe 500 with rollback; the read path never commits.

These are local implementation choices where design evidence is incomplete, not owner-approved business/schema decisions.

## Limits

- Fake DB tests do not establish PostgreSQL schema, grants, migration state, deployment or production behavior.
- The role-only guard does not prove that the separate course-management permission in AC-32 is enforced.
- Counter definitions, category relation, nullable/orphan projection handling and CourseStatus enum/casing remain unresolved; document status stays `Draft — Needs Confirmation`.
