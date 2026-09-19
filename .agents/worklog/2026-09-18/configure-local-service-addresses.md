---
task_id: "2026-09-18-configure-local-service-addresses"
date: "2026-09-18"
primary_task_type: "coding"
secondary_task_types: ["docs", "context-update", "test"]
project_scopes: ["server-ai", "db-admin", "server-work", "server-study", "web-work"]
cross_scope_dependencies:
  - "DB Admin client 127.0.0.2:3000 -> DB Admin server 127.0.0.1:3001"
  - "Work client 127.0.0.2:3001 -> Work server 127.0.0.1:3002"
  - "Study client 127.0.0.2:3002 -> Study server 127.0.0.1:3003"
status: "PARTIAL"
---

# Worklog: Chuẩn hóa địa chỉ khởi tạo Study2Work

## EXPECTED_BEHAVIOR

- AI server: `127.0.0.1:3000`.
- DB Admin server/client: `127.0.0.1:3001` / `127.0.0.2:3000`.
- Work server/client: `127.0.0.1:3002` / `127.0.0.2:3001`.
- Study server/client: `127.0.0.1:3003` / `127.0.0.2:3002`.
- Preserve PostgreSQL, Redis, Ollama and test fixture addresses.
- Record the mapping in `docs/gui/deploy/ip.md` and relevant `.agents` pages.

## CURRENT_BEHAVIOR

- Runtime launchers, Vite settings, server defaults, proxy targets, CORS and
  local startup documentation now use the requested application map.
- Work server now carries a configured host and passes it to `app.listen`.
- Docker Compose app host ports were updated; containerized Study startup keeps
  its internal `0.0.0.0` bind.
- Ollama and database/cache addresses were not changed.

## SOURCE_TRACE

```text
local launcher/package script
  -> host/port binding or Vite dev server
  -> client proxy/API base/CORS
  -> application health/root endpoint

DB Admin: scripts/dev.mjs -> Angular/proxy.conf.json -> FastAPI /health/live
Work: constants.ts -> core/config.ts -> main.ts -> Express /api/v1
Study: constants.py/Dockerfile -> uvicorn -> FastAPI /health/live
AI: documented uvicorn command -> FastAPI /api/v1/chat_log_ai -> Ollama
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Context registry snapshot | Validator reports pre-existing `CONTEXT_STALE` across server-work, server-study, web-work and db-admin source roots | `CONTEXT_STALE` | Did not change `sourceCommit` as a shortcut; recorded current address updates in affected pages |
| Docker validation | `docker compose config --quiet` cannot run because `docker` is unavailable | `DECLARED_NOT_RUNNABLE` | Compose syntax/runtime was not executed locally |
| Study full suite | Collection stops at stale `app.modules.auth.view` import | `DECLARED_NOT_RUNNABLE` | Focused Study config/health tests were run instead |
| Angular full Vitest run | Deno runner lacks Angular JIT/compiler integration; existing Node test file is not a Vitest suite | `DECLARED_NOT_RUNNABLE` | Angular production build and DB Admin launcher test were checked separately |
| Work Compose build | Existing Compose references `apps/work-server/Dockerfile`, which is absent | `SOURCE_REQUIRED` | Address mapping was updated without repairing the unrelated build boundary |

## CHANGES

- Runtime/config: AI startup docs; DB Admin launcher/proxy/config/CORS; Work
  host/port config and Vite proxy; Study client/server defaults, CORS and
  container port; Compose app mappings.
- Documentation: README/infra docs and `docs/gui/deploy/ip.md`.
- Context pages: project architecture/dependencies/source-status, server AI,
  DB Admin, Work server, Study runtime, Work Web and Study Web.
- Tests: DB Admin launcher/config assertions, Work config/app/client origin,
  Study default CORS assertion.
- Credentials: no credential value was added to documentation, tests or logs;
  only existing host/port/CORS fields were edited in local constants.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `git diff --check` | Passed | `VERIFIED` |
| DB Admin `.venv/bin/pytest -q` | 45 passed | `VERIFIED` |
| `deno test --allow-all apps/db-admin-web/scripts/dev.test.mjs` | 2 passed | `VERIFIED` |
| Focused Work/Work Web/Study Web Vitest run | 26 tests passed | `VERIFIED` |
| Work TypeScript check via installed compiler/Deno | Passed | `VERIFIED` |
| Work Web TypeScript check via installed compiler/Deno | Passed | `VERIFIED` |
| Study Web `vue-tsc --noEmit` via Deno | Passed | `VERIFIED` |
| Study focused pytest (`test_config.py`, `test_health.py`) | 12 passed | `VERIFIED` |
| AI `compileall` | Passed | `VERIFIED` |
| Angular production build via Deno | Bundle generated successfully; wrapper did not exit cleanly | `PARTIAL` |
| `docker compose config --quiet` | `docker: command not found` | `DECLARED_NOT_RUNNABLE` |
| `deno run ... scripts/validate-agent-context.mjs` | Reports pre-existing source drift as `CONTEXT_STALE` | `PARTIAL` |

## HANDOFF

- Remaining blockers: Docker is unavailable; Node/uv are unavailable on PATH;
  full Study collection and canonical context validator remain blocked by
  existing repository drift/import issues.
- Next owner/action: run canonical Node/Compose checks in a full toolchain and
  reconcile the broader context snapshot before marking the repository context
  fully verified.
