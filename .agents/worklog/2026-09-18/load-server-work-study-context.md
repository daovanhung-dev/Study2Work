---
task_id: "2026-09-18-load-server-work-study-context"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["server-work", "server-study"]
cross_scope_dependencies: ["contracts/events/study-work/ — Study producer, Work consumer chưa implement"]
status: "PARTIAL"
---

# Worklog: Nạp context Work Server và Study Server

## EXPECTED_BEHAVIOR

- Nạp root router, context registry, project boundary và page graph đầy đủ cho `server-work` và `server-study`.
- Đối chiếu các source bắt buộc với working tree hiện tại; giữ riêng expected/current behavior.
- Không sửa business code, API, schema hoặc contract khi yêu cầu chỉ là nạp context.

## CURRENT_BEHAVIOR

- Work Server: Express 4 + TypeScript + Prisma/PostgreSQL/Neon; JSON API-only dưới `/api/v1`; JWT Bearer stateless; schema Prisma 12 model.
- Work auth hiện dùng bcrypt cost 12 cho account mới, hỗ trợ legacy plaintext login và best-effort rehash; public selects loại `matkhau`.
- Study Server: FastAPI + sync SQLAlchemy; composition root và route register hiện import được; login/refresh/me/chat chưa wired.
- Study register flow: `RegisterRequest` → duplicate lookup → Argon2id hash → `INSERT users` → commit → safe response.
- Study pytest collection còn bị block bởi stale import `app.modules.auth.models/view`; live DB metadata chưa được xác minh.

## SOURCE_TRACE

```text
.agents/AGENTS.md
-> .agents/context-manifest.json
-> .agents/project/{INDEX,architecture,dependencies,contracts,workflows}.md
-> .agents/server-work/{AGENTS,INDEX,architecture,apis,core,database,modules,tests,workflows}
-> apps/work-server/src/app.ts -> routes/api_routes.ts
-> auth.middleware.ts -> utils/jwt.ts -> services/* -> shared Prisma -> prisma/schema.prisma
-> .agents/server-study/{AGENTS,INDEX,architecture,apis,core,database,modules,services,tests,workflows}
-> apps/study-server/app/main.py -> api/v1.py
-> register_account/{models,query,validate,view}.py -> core/database.py/responses.py
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Work context source snapshot | Manifest `sourceCommit=9a70eb6`; current `HEAD=50c6e78`; validator reports drift in Work source including auth/router/schema/migration | `CONTEXT_STALE` | Context đã nạp để định hướng, nhưng claim chi tiết phải ưu tiên current source khi coding/fix |
| Study register test collection | `tests/modules/auth/test_register.py` imports removed `app.modules.auth.models/view` | `DECLARED_NOT_RUNNABLE` | Không dùng stale test làm runtime evidence |
| Study live schema | Current register SQL references `users`; live metadata chưa kiểm tra | `SOURCE_REQUIRED` | Không suy diễn thêm table/column/constraint |
| Study → Work event consumer | `contracts/events/study-work/` có schemas nhưng Work consumer chưa có | `DECLARED_NOT_RUNNABLE` | Không coi event schema là implementation |
| Node validator | `node` không có trong shell | `DECLARED_NOT_RUNNABLE` | Dùng Deno compatibility invocation |

## CHANGES

- Files changed: thêm worklog này; không sửa Work/Study source, test, schema hoặc contract.
- CONTEXT_UPDATES: không refresh manifest/page graph vì yêu cầu chỉ nạp context; ghi nhận drift để task sau xử lý có chủ đích.
- Context pages changed: none.
- Assumptions: “nạp context work-server và study-server” bao gồm project boundary vì hai scope được yêu cầu cùng lúc.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Đọc current source bắt buộc của Work và Study | Source đối chiếu được; working tree sạch | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | `node: command not found` | `DECLARED_NOT_RUNNABLE` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs` | `Contract validation passed` | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | `CONTEXT_STALE server-work` | `CONTEXT_STALE` |

## HANDOFF

- Remaining blockers: Work context cần refresh theo source snapshot hiện tại trước khi dùng như bằng chứng độc lập; Study pytest collection và live DB metadata vẫn chưa verified.
- Next owner/action: task coding/fix tiếp theo phải bắt đầu từ current source, sau đó trace route → middleware/core → service/query → DB side effect → response → tests; nếu chỉnh contract/context thì refresh page tương ứng và chạy validator bằng Deno khi Node chưa có.
