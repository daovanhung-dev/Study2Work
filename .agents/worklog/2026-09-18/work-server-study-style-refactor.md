---
task_id: "2026-09-18-work-server-study-style-refactor"
date: "2026-09-18"
primary_task_type: "coding"
secondary_task_types: ["fix", "test", "docs"]
project_scopes: ["server-work", "server-study"]
cross_scope_dependencies: ["contracts/openapi/work/legacy-web.openapi.json", "contracts/openapi/work/openapi.json", "apps/work-client/web/src/shared/api/work.ts"]
status: "COMPLETED_WITH_UNCOMMITTED_CONTEXT_DRIFT"
---

# Worklog: Refactor Work Server theo kiến trúc Study-style

## EXPECTED_BEHAVIOR

- Refactor Work request lifecycle theo Study-style: composition root → middleware → API router → models/validate → view/use-case → query/repository → Prisma → canonical response/error.
- Giữ nguyên current Work route paths, request fields, HTTP statuses, business codes, password compatibility và Work Web behavior.
- Bổ sung `GET /api/v1`, `/health/live`, `/health/ready` theo Work OpenAPI; không triển khai target domain chưa wired.
- Thêm dependency injection và HTTP integration tests dùng fake dependencies, không kết nối Neon.

## CURRENT_BEHAVIOR

- Work now exposes `createApp(options)` and keeps bootstrap/connect/listen/shutdown
  in `main.ts`; trace, config, DI, responses, exceptions and security are wired
  under `src/core/`.
- `src/api/v1.ts` composes current compatibility routes and system routes; each
  wired domain is split into `models/validate/view/query/routes`, with injected
  Prisma query boundaries and transaction-backed compound mutations.
- `routes/api_routes.ts` and `config/prisma.config.ts` remain compatibility
  adapters; legacy services still exist but are not in the new route graph.
- Work has an injected fake-Prisma Vitest/Supertest suite; Work Web remains
  unchanged at the public API boundary and its typecheck/tests pass.

## SOURCE_TRACE

```text
apps/work-server/src/main.ts
-> src/app.ts (`createApp(options)`)
-> src/core/{config,database,dependencies,trace,responses,exceptions,middleware}
-> src/middleware/auth.middleware.ts + src/core/security/*
-> src/api/v1.ts
-> src/modules/{auth,students,businesses,jobs,cv,applications}/{models,validate,view,query,routes}
-> prisma/schema.prisma
-> contracts/openapi/work/{legacy-web.openapi.json,openapi.json}
-> apps/work-client/web/src/shared/api/work.ts
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Work runtime architecture | Legacy monolithic Express route/service source was migrated to Study-style module boundaries | `VERIFIED` | Public route/field/status/business-code compatibility retained in focused tests |
| Work target OpenAPI | `openapi.json` defines system routes and broader target domains; only system routes are wired | `DISCREPANCY` | Do not wire tenant/billing/university/interview/storage/webhook operations |
| Work server tests | Injected Vitest + Supertest suite is now checked in | `VERIFIED` | 12 HTTP tests pass without Neon/Docker |
| Work package locks | `pnpm-lock.yaml` graph updated; `package-lock.json` is retained unchanged as a legacy lock because npm resolver generation was blocked in this shell | `VERIFIED` / `DECLARED_NOT_RUNNABLE` | `pnpm@9.15.4` is the repository package manager; do not run npm ci against the legacy lock without an explicit lock migration |
| Work context snapshot | Manifest source snapshot predates this uncommitted source change | `CONTEXT_STALE` | Context pages and registry were refreshed; full validator correctly reports uncommitted drift |
| Node runtime | Initial shell lacked Node; temporary Node 22 binary was used for canonical checks | `VERIFIED_WITH_FALLBACK` | No binary or secret was added to the repository |

## CHANGES

- Added typed environment config, Prisma factory/DI, trace AsyncLocalStorage,
  canonical envelope/error helpers, centralized exception mapping, async handler,
  HS256 access-token helper and password compatibility adapter under `src/core/`.
- Converted `main.ts` to bootstrap/connect/listen/shutdown only; converted
  `app.ts` to `createApp(options)` and added `/api/v1`, live and ready system routes.
- Moved current auth, student, business, jobs, CV and application flows into
  `models/validate/view/query/routes` modules; kept `routes/api_routes.ts` as a
  compatibility re-export and preserved the Prisma schema/migrations.
- Added 12-test Supertest/Vitest injected fake-Prisma suite, Zod body/query/path
  models, transaction boundaries for compound mutations, package scripts and
  the canonical pnpm dependency lock update.
- Updated Work README, `.env.example`, OpenAPI status README and affected
  `.agents/server-work` plus `.agents/project/source-status.md` pages.
- Assumptions: Work configuration remains environment-driven; no Prisma schema
  or migration changes; target domains outside system routes remain unwired.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Source/context/contract inspection | Plan, Study composition pattern, legacy OpenAPI and current route boundaries verified | `VERIFIED` |
| `npm run typecheck` in Work Server | `tsc --noEmit` | `VERIFIED` |
| `npm test` in Work Server | 12 tests passed | `VERIFIED` |
| `npm run prisma:validate` in Work Server | Valid with non-secret dummy database URLs | `VERIFIED` |
| `npm run contracts:validate` at repository root | Contract validation passed | `VERIFIED` |
| Work Web typecheck/tests | Typecheck passed; 5 tests passed | `VERIFIED` |
| `validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | `VERIFIED` |
| `validate-agent-context.mjs` | Fails only with `CONTEXT_STALE` for uncommitted source changes relative to manifest snapshot | `CONTEXT_STALE` |

## HANDOFF

- Implementation and focused verification are complete.
- Before merging/committing, run the canonical npm/pnpm commands in a normal
  Node environment, then update `sourceCommit` in `.agents/context-manifest.json`
  to the commit that contains this source/context refresh and rerun the full
  context validator.
