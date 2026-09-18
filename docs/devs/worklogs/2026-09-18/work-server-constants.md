---
task_id: "2026-09-18-work-server-constants"
date: "2026-09-18"
primary_task_type: "fix"
secondary_task_types: ["coding", "security-review", "docs", "test"]
project_scopes: ["server-work", "server-study"]
cross_scope_dependencies: [".agents/context-manifest.json", "apps/study-server/app/core/constants.py"]
status: "PARTIAL"
---

# Worklog: Work Server static constants configuration

## EXPECTED_BEHAVIOR

- Requirement: Work runtime configuration and secret values come from static `src/utils/constants.ts`, never `.env` or `process.env`.
- Canonical contract/approved DD: Preserve existing Work routes, Prisma schema, JWT claims, response envelopes and injected test configuration.
- Follow-up requirement: the single Work configuration authority is the tracked `src/utils/constants.ts`; the previous root constants files are removed.
- Follow-up requirement: use the operator-provided Neon URL for both Prisma URL fields, generate a new HS256 JWT secret locally, and leave unwired Redis/Supabase values empty.

## CURRENT_BEHAVIOR

- Before this change, `src/core/config.ts` read `process.env`; `src/utils/constants.ts` re-exported the ignored root constants. After this change, the tracked `src/utils/constants.ts` is the sole static configuration source.
- Runnable tests: `test/app.test.ts` injects `WorkConfig` and fake Prisma; `test/config.test.ts` also verifies the default static configuration without opening a database connection.
- Runtime wiring: `main.ts`, Prisma compatibility config, JWT helpers and CLI wrapper now receive values from `src/utils/constants.ts`. The CLI wrapper still inherits non-configuration process environment for child-process execution and explicitly overrides Prisma URLs from constants.
- Root constants/template files are absent; the supplied Neon target and newly generated HS256 secret are configured only in the static constants module.

## SOURCE_TRACE

```text
main/prisma.config/utils/jwt -> loadConfig -> src/utils/constants.ts -> WorkConfig -> Prisma/JWT/Express
scripts/prisma-with-constants -> utils/constants -> src/utils/constants.ts -> child process DATABASE_URL/DIRECT_DATABASE_URL
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Work runtime source | `apps/work-server/src/core/config.ts` imports `src/utils/constants.ts`; no runtime `process.env`/`.env` read remains under `src/` | RESOLVED | Required runtime values now cross the static constants boundary |
| Work runtime credential | Operator supplied the Neon target and authorized a newly generated local HS256 secret | RESOLVED | Runtime config is available without `.env` |
| Study pattern | `apps/study-server/app/core/constants.py` is static configuration | VERIFIED | Architecture reference only; no Study credential reuse |
| Work constants authority | Root constants were removed; `src/utils/constants.ts` is the tracked authority | RESOLVED | Source, context and docs are aligned |

## CHANGES

- Files changed: Work constants/config/tests, `.env.example`, README, agent context pages, context manifest and this worklog; root constants/template files removed.
- CONTEXT_UPDATES: Document tracked `src/utils/constants.ts` as the Work runtime configuration boundary.
- Context pages changed: project conventions, Work AGENTS, Work architecture, Work auth/config/database, Work workflows/tests and project source status.
- Assumptions: the operator explicitly authorized the supplied Neon URL and a newly generated JWT secret in tracked `src/utils/constants.ts`; no credential is copied into context, docs, tests, logs or reports.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Runtime/static scan | No `process.env`/`dotenv`/`.env` references under `apps/work-server/src`; no root constants import or example reference | PASS |
| TypeScript compiler API fallback | `TypeScript diagnostics: 0 (66 files)` via Deno + local TypeScript 5.7.3 | PASS |
| Work Vitest fallback | 2 files, 17 tests passed, including default static-source and process-environment regression tests | PASS |
| Prisma wrapper fallback | Deno `--sloppy-imports ... prisma-with-constants.ts validate`; schema valid | PASS |
| `pnpm --filter work_server typecheck` | `pnpm: command not found` | DECLARED_NOT_RUNNABLE |
| `pnpm --filter work_server test` | `pnpm: command not found` | DECLARED_NOT_RUNNABLE |
| `pnpm --filter work_server prisma:validate` | `pnpm: command not found`; Deno fallback passed schema validation | DECLARED_NOT_RUNNABLE |
| `pnpm contracts:validate` | `pnpm: command not found`; Deno contract fallback was run separately | DECLARED_NOT_RUNNABLE |
| `deno run ... scripts/validate-contracts.mjs` | `Contract validation passed.` | PASS |
| `deno run ... scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | PASS |
| Exact agent-context validator | Existing source snapshot mismatch reports `CONTEXT_STALE server-work` across prior refactor files | CONTEXT_STALE |
| `git diff --check` and credential-location scan | Clean diff; supplied database target occurs only in `src/utils/constants.ts`; no credential copied to docs/context/worklog | PASS |

## HANDOFF

- Remaining blockers: Node/pnpm availability and live database smoke verification still depend on the execution environment. The agent context source snapshot is stale for the prior Work refactor and is intentionally not relabeled as current.
- Next owner/action: Run the canonical Node/pnpm checks in an environment with the declared toolchain; do not copy Study credentials or values from Git history.
