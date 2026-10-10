---
task_id: "2026-10-04-study-db-schema-per-transaction-reapply"
date: "2026-10-04"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Khôi phục DB_SCHEMA theo từng transaction cho Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-28/remove-study-apiresponse.md`
    - carry_forward: Preserve unrelated worktree changes; run focused and full Study tests plus static checks.
  - path: `.agents/worklog/2026-09-28/study-apierror-direct-json.md`
    - carry_forward: Keep Study scope limited, use Deno for context validation when Node is unavailable, and record repository-wide context failures as baseline when unrelated.
  - path: `.agents/worklog/2026-09-28/study-apierror-factory.md`
    - carry_forward: Keep runtime/source evidence above stale context and preserve transaction ownership in DB callers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Reapply the approved plan so each PostgreSQL transaction sets the configured `Settings.db_schema` before business SQL runs.
- Canonical contract/approved plan: Attach SQLAlchemy `begin` listener to PostgreSQL engines; execute parameterized `SELECT set_config('search_path', quote_ident(:schema), true)`; allow setup errors to abort the transaction; preserve pooled Neon URL and pool settings; do not add `public`, change config/constants structure, or send schema in startup options.

## CURRENT_BEHAVIOR

- Source/config: `Settings.db_schema` is validated and sourced from `DB_SCHEMA`, but `build_engine()` currently returns `create_engine(...)` without using it. The engine is created from `main.create_app()` and cached `get_engine()`; direct test DB and module views use this engine/session path.
- Runnable tests: `tests/core/test_database.py` currently checks URL parsing, pool options without startup search path, query mapping, and session close. `.agents/server-study/tests.md` reports 163 tests; this turn will establish current runnable results.
- Runtime wiring: API DB sessions flow through `get_db()`/`get_db_from_factory()` into views; `/api/v1/test/db` opens `get_engine().connect()`. Query helpers do not commit; callers/views own transactions.

## SOURCE_TRACE

```text
main.create_app / get_engine -> build_engine -> PostgreSQL SQLAlchemy Engine
Engine transaction begin -> configured-schema listener -> transaction-local set_config
API route -> get_db -> Session -> view -> query_one/query_many/execute_query -> caller-owned transaction
/api/v1/test/db -> get_engine().connect() -> SELECT NOW() -> connection close
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Configured schema not applied | `Settings.db_schema` exists and validates, but current `build_engine()` does not register a begin listener | DISCREPANCY | Restore transaction-local schema setup before DB queries. |
| Live Neon schema | No live database metadata check is part of this task | NOT_VERIFIED_HERE | Unit tests establish listener behavior only; schema existence/permissions remain unverified. |

## CHANGES

- Files changed: `apps/study-server/app/core/database.py`, `apps/study-server/tests/core/test_database.py`, `.agents/server-study/AGENTS.md`, `.agents/server-study/core/database-security.md`, `.agents/server-study/database.md`, `.agents/server-study/tests.md`, and this worklog.
- CONTEXT_UPDATES: Documented PostgreSQL transaction-local schema selection, its error behavior, the absence of a `public` fallback/schema creation, and the verified 165-test count.
- Context pages changed: `.agents/server-study/AGENTS.md`, `.agents/server-study/core/database-security.md`, `.agents/server-study/database.md`, `.agents/server-study/tests.md`.
- Assumptions: Use only the configured schema and retain Neon transaction-pooler URL; do not create schemas or use a `public` fallback.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `cd apps/study-server && .venv/bin/pytest tests/core/test_database.py -q` | `7 passed, 1 existing Starlette/httpx deprecation warning` | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest -q` | `165 passed, 1 existing Starlette/httpx deprecation warning` | VERIFIED |
| `cd apps/study-server && .venv/bin/ruff check app/core/database.py tests/core/test_database.py` | All checks passed | VERIFIED |
| `git diff --check` | No whitespace errors | VERIFIED |
| `deno run -A scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`: repository baseline has missing DB Admin pages/source and stale context snapshots across scopes | CONTEXT_BASELINE |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Still invalid due missing DB Admin pages/source and broken DB Admin links; Study-specific structure is not identified as a failure | CONTEXT_BASELINE |
| Live Neon connection/schema probe | Not run; unit test uses fake engine/connection and no database writes | NOT_RUN |

## HANDOFF

- Remaining blockers: Repository-wide context validation remains blocked by absent DB Admin context/source paths and stale tracked snapshots; configured live schema existence/permissions were not probed.
- Next owner/action: None for this implementation; resolve the repository-wide context baseline separately if required.
