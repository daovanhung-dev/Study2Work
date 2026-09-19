---
task_id: "2026-09-18-load-work-domain-context"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: ["context-loading"]
project_scopes: ["server-work", "web-work", "mobile-work"]
cross_scope_dependencies:
  - "Work Web -> relative /api/v1 -> Work Server"
  - "Work Mobile -> direct Neon PostgreSQL/SQLite cache; không đi qua Work Server"
status: "PARTIAL"
---

# Worklog: Nạp context Work domain

## EXPECTED_BEHAVIOR

- Nạp context theo registry cho ba boundary Work: server, web và mobile.
- Giữ riêng expected/current behavior và không suy diễn route hoặc contract từ file chưa được wire.

## CURRENT_BEHAVIOR

- Work Server: Express 4 + TypeScript + Prisma/PostgreSQL/Neon, JSON API dưới `/api/v1`, JWT Bearer stateless.
- Work Web: React + TypeScript + Vite, gọi relative `/api/v1`, parse envelope/Zod, lưu `access_token`; không dùng cookie/session hoặc Neon credential.
- Work Mobile: hai Flutter app độc lập, direct Neon SQL + SQLite cache; chat polling 3 giây; AI gọi Gemini trực tiếp.
- Worktree sạch; không sửa source ứng dụng.

## SOURCE_TRACE

```text
Work Web router/page -> shared/api/work.ts -> relative /api/v1
  -> apps/work-server/src/app.ts -> src/api/v1.ts -> module route
  -> auth/middleware + view/query -> injected Prisma -> prisma/schema.prisma

Work Mobile view -> controller -> helper_db/neon_db.dart -> Neon PostgreSQL
  -> SQLite session/cache; AIService -> Gemini HTTP API
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Work OpenAPI | `legacy-web.openapi.json` aligns with current server routes; larger `openapi.json` target is not fully wired | `DISCREPANCY` | API changes must trace current route source and legacy contract |
| Study -> Work events | Schemas exist but Work consumer is absent | `DECLARED_NOT_RUNNABLE` | Không suy diễn signature/idempotency/persistence từ schema |
| Work Server source status | Registry marks `server-work` as `SOURCE_CHANGED` relative to context snapshot | `SOURCE_CHANGED` | Exact source must be rechecked before edits |
| Context validator | `node scripts/validate-agent-context.mjs` could not run because `node` is unavailable | `DECLARED_NOT_RUNNABLE` | Context validation remains pending |

## CHANGES

- Files changed: added this worklog only.
- CONTEXT_UPDATES: none; context pages already cover the loaded boundaries.
- Context pages changed: none.
- Assumptions: “Work” means the Work Server, Work Web and Work Mobile boundaries.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Read registry, scope entries/pages and exact Work Server source | Completed for server, web and mobile context | `VERIFIED` |
| `git status --short` | No pre-existing source changes observed | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | `node` is unavailable in the shell | `DECLARED_NOT_RUNNABLE` |

## HANDOFF

- Remaining blockers: context validator and Node/TypeScript checks require a Node-enabled environment.
- Next owner/action: for a concrete change, select the affected boundary and trace its exact route/module/helper/test path before editing.
