---
task_id: "2026-09-21-build-work-projects"
date: "2026-09-21"
primary_task_type: "test"
secondary_task_types: ["docs"]
project_scopes: ["server-work", "web-work"]
cross_scope_dependencies: ["Work Web relative /api/v1 proxy -> Work Server API"]
status: "VERIFIED"
---

# Worklog: Build Work Server và Work Web

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-18/work-server-api-tests.md`
    - carry_forward: canonical pnpm commands remain unavailable; Deno fallback is an accepted verification path; Work Server tests use injected fake Prisma and do not connect to Neon.
- shortage: `2 missing` (1 matching worklog available; all available logs were read)

## EXPECTED_BEHAVIOR

- Requirement: Build Work Server and Work Web, including type checking, server compilation, Prisma validation/client generation, and production web bundling.
- Canonical contract/approved DD: Work Server uses TypeScript/Prisma and exposes the API mounted at `/api/v1`; Work Web uses React/Vite and proxies `/api`, `/uploads`, and `/img` to Work Server.

## CURRENT_BEHAVIOR

- Source/config: `apps/work-server` has no dedicated build script; its TypeScript source is executed through `ts-node`, while Prisma provides schema validation/client generation. `apps/work-client/web` uses `tsc --noEmit && vite build`.
- Runnable tests: Build checks run through local dependency entrypoints with Deno because Node/Corepack/pnpm are unavailable.
- Runtime wiring: Work Web production bundle builds independently; no server process or live database connection was started.

## SOURCE_TRACE

```text
Work Web package build -> TypeScript compiler -> Vite index.html/src -> production assets
Work Server source -> TypeScript compiler -> temporary JS output
Work Server prisma/schema.prisma -> Prisma CLI -> schema validation + generated Prisma Client
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Canonical `corepack pnpm` build commands | `node`, `npm`, `corepack`, and `pnpm` are not installed in the environment | DECLARED_NOT_RUNNABLE | Canonical package-script execution is not independently verified; equivalent local Deno fallback passed |
| Live Work Server startup/database smoke test | Build task does not start `src/main.ts`; Prisma checks use placeholder URLs and do not connect to Neon | OUT_OF_SCOPE | Runtime/deployment readiness is not claimed |

## CHANGES

- Files changed: `.agents/worklog/2026-09-21/build-work-projects.md` only; no runtime/API/schema source changed.
- CONTEXT_UPDATES: None; existing context remains sufficient for this build verification.
- Context pages changed: None.
- Assumptions: Temporary compiler and Vite outputs are build artifacts outside the repository; generated Prisma files remain dependency artifacts.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Deno TypeScript check for Work Server | Exit 0 | VERIFIED_FALLBACK |
| Deno TypeScript emit for Work Server to `/tmp` | Exit 0 | VERIFIED_FALLBACK |
| Deno Prisma validate with placeholder PostgreSQL URLs | Schema valid | VERIFIED_FALLBACK |
| Deno Prisma generate | Prisma Client v6.19.3 generated | VERIFIED_FALLBACK |
| Deno TypeScript check for Work Web | Exit 0 | VERIFIED_FALLBACK |
| Deno Vite production build from `apps/work-client/web` | 108 modules transformed; `index.html`, JS and CSS generated | VERIFIED_FALLBACK |
| `git diff --check` | Clean | PASS |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | PASS |

## HANDOFF

- Remaining blockers: Install Node/Corepack to verify the canonical `corepack pnpm` commands; no live API/database smoke test was performed.
- Next owner/action: Re-run the canonical Work Server/Web package commands in a Node-enabled environment before deployment.
