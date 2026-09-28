---
task_id: "2026-09-19-load-server-study-context"
date: "2026-09-19"
primary_task_type: "docs"
secondary_task_types: ["context-loading", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nạp context Study Server

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/2026-09-19-create-mobile-dd.md`
    - carry_forward: Context phải source-backed; Deno là compatibility runner khi Node không có; không claim runtime khi toolchain thiếu.
  - path: `.agents/worklog/2026-09-19/2026-09-19-upgrade-agent-workflow-worklog.md`
    - carry_forward: Selector/worklog/validator là workflow bắt buộc; registry và page graph phải được đọc cùng nhau.
  - path: `.agents/worklog/2026-09-19/create-agent-context-map.md`
    - carry_forward: Phải đọc context-map trước khi chọn scope; không suy diễn runtime từ tên file; full validator có thể báo source drift.
- shortage: `none`

## EXPECTED_BEHAVIOR

- User request: nạp context dự án `server-study` để các task tiếp theo dùng đúng scope, boundary, source và verification status.
- Canonical load: `.agents/AGENTS.md` → `.agents/context-map.md` → `server-study/AGENTS.md` → `server-study/INDEX.md` → các page architecture/API/core/database/module/service/tests/workflow.

## CURRENT_BEHAVIOR

- Source root: `apps/study-server/`; current HEAD `8da2a7f4a00427293c69fb8aae96dd085f6808fd`.
- Composition import: `app.main:app` imports successfully from the project virtualenv.
- Current OpenAPI paths: `/`, `/health/live`, `/health/ready`, `/api/v1/hello`, `/api/v1/test/db`, `/api/v1/auth/register`.
- Focused runnable tests: 28 passed for core, AI service, health and security test groups.
- Full pytest collection: blocked by stale imports in `tests/modules/auth/test_register.py` (`app.modules.auth.view` and `app.modules.auth.models`), while current runtime module is `app.modules.auth.register_account`.
- Database live availability: not probed; source only establishes the Neon URL and sync SQLAlchemy helpers.
- Runtime wiring: register account is wired; login, refresh, current-user and Study chat-log flows are not exposed.

## SOURCE_TRACE

```text
app/main.py:create_app
-> app/api/v1.py:router
-> app/modules/auth/register_account/{models,view,query}.py
-> app/core/database.py + app/core/security/password.py + app/core/responses.py
-> POST /api/v1/auth/register
-> focused tests pass; stale register test module blocks full collection
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Full Study pytest suite | `tests/modules/auth/test_register.py` imports removed `app.modules.auth.view/models` | DECLARED_NOT_RUNNABLE | Do not claim full-suite verification until test imports are reconciled by an approved fix |
| Database schema/live metadata | `database.md`, current source and register SQL; no live probe performed | SOURCE_BACKED / LIVE_NOT_VERIFIED | Do not infer table/column availability from design docs or config |
| Context route count | `server-study/AGENTS.md` says 8 current routes; current OpenAPI exposes 6 paths | DISCREPANCY | Prefer current source/OpenAPI for subsequent runtime descriptions |
| Login/refresh/me/chat | Route declarations are absent from current `app/api/v1.py` | UNWIRED | Do not copy legacy or AI Server behavior without a requirement/contract |

## CHANGES

- Files changed: `.agents/worklog/2026-09-19/load-server-study-context.md` only.
- CONTEXT_UPDATES: none; this task loaded and checked existing context.
- Context pages changed: none.
- Assumptions: no business behavior was requested; current source and runnable focused tests take precedence over stale context wording.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read 3 matching worklogs | VERIFIED |
| `cd apps/study-server && .venv/bin/python -c 'from app.main import app; ...'` | Composition root imported; current OpenAPI paths inspected | VERIFIED |
| `cd apps/study-server && .venv/bin/pytest --collect-only -q` | 28 collected, register module collection error | DECLARED_NOT_RUNNABLE |
| `cd apps/study-server && .venv/bin/pytest -q tests/core tests/service/ai tests/test_health.py tests/test_security.py` | 28 passed, 1 deprecation warning | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing `CONTEXT_STALE` in Study plus other scopes | CONTEXT_STALE |

## HANDOFF

- Remaining blockers: stale register test import; live database/schema status not verified; context route-count wording is stale against current OpenAPI; full validator reports existing source drift in Study/Work/Web/DB Admin scopes.
- Next owner/action: for a register fix, trace and reconcile the stale test imports first, then run focused register tests and full Study collection; for DB work, obtain authoritative live schema evidence.
