---
task_id: "2026-09-18-work-server-api-tests"
date: "2026-09-18"
primary_task_type: "test"
secondary_task_types: ["coding", "docs"]
project_scopes: ["server-work"]
cross_scope_dependencies: ["contracts/openapi/work/legacy-web.openapi.json"]
status: "PARTIAL"
---

# Worklog: Work Server API integration coverage

## EXPECTED_BEHAVIOR

- Test all 21 currently wired Work runtime routes through Supertest and the injected fake Prisma boundary.
- Preserve route paths, status codes, business codes, response envelopes, auth behavior, serialization and upload limits.
- Do not connect Neon, Docker or any live database during the API test suite.

## CURRENT_BEHAVIOR

- `apps/work-server/test/app.test.ts` now has 15 HTTP tests covering the system foundation, both auth roles, `/me`, registration, jobs, applications, CV ownership/read paths, business job CRUD, unexpected failures and upload failures.
- `apps/work-server/test/config.test.ts` has 5 static-configuration tests.
- Current suite passes 20 tests and includes an explicit 21-route runtime inventory. The HTTP tests use injected fake Prisma and do not open Neon.

## DISCREPANCIES

| Item | Status | Evidence |
|---|---|---|
| Full 21-route HTTP coverage | RESOLVED | Route inventory and grouped HTTP tests cover all currently wired system, auth, student, job, CV and application endpoints |
| Live database smoke test | OUT_OF_SCOPE | Existing test boundary injects fake Prisma and does not require Neon/Docker |
| API contract compatibility | VERIFIED_BASELINE | Existing route source and legacy Work OpenAPI remain unchanged before test expansion |

## SOURCE_READ

- `apps/work-server/src/api/v1.ts`
- `apps/work-server/src/app.ts`
- `apps/work-server/src/modules/*/routes.ts`
- `apps/work-server/src/modules/*/view.ts`
- `apps/work-server/src/modules/*/query.ts`
- `apps/work-server/src/core/responses.ts`
- `apps/work-server/src/core/exceptions.ts`
- `apps/work-server/src/config/multer.ts`
- `apps/work-server/test/app.test.ts`

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Baseline Deno Vitest fallback | 2 files, 17 tests passed | PASS |
| Deno Vitest fallback | 2 files, 20 tests passed (15 HTTP + 5 config) | PASS |
| TypeScript compiler API fallback | `TypeScript diagnostics: 0 (66 files)` | PASS |
| Prisma/contract runtime source | No Work runtime source changed by this test task | VERIFIED_BASELINE |
| `pnpm --filter work_server typecheck` | `pnpm: command not found` | DECLARED_NOT_RUNNABLE |
| `pnpm --filter work_server test` | `pnpm: command not found`; Deno fallback passed | DECLARED_NOT_RUNNABLE |
| `pnpm contracts:validate` | `pnpm: command not found`; Deno contract validator passed | DECLARED_NOT_RUNNABLE |
| Agent context validator | Existing Work source snapshot reports `CONTEXT_STALE`; `--skip-drift` passes | CONTEXT_STALE |
| `git diff --check` | Clean | PASS |

## HANDOFF

- Completed action: extended the existing fake Prisma/store and HTTP assertions without modifying route/runtime behavior.
- Remaining limitation: canonical pnpm commands are unavailable in this environment and the pre-existing Work context snapshot remains stale.
