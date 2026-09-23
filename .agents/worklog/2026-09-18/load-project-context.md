---
task_id: "2026-09-18-load-project-context"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study", "server-work"]
cross_scope_dependencies: ["Study Web -> Study API boundary; Work Web/Work API boundary; Study -> Work events remain unwired"]
status: "PARTIAL"
---

# Worklog: Nạp context dự án

## EXPECTED_BEHAVIOR

- Nạp root router, registry, project boundary và scope context tương ứng với các file đang mở.
- Giữ riêng expected/current behavior và không sửa business code khi yêu cầu chỉ là nạp context.

## CURRENT_BEHAVIOR

- Study Web là Vue 3 + Vite skeleton; route hiện tại chỉ có `/`, HTTP helper chưa có caller, Study OpenAPI là placeholder.
- Study API là FastAPI + sync SQLAlchemy; composition hiện import được, register là flow business đang có; login/refresh/me/chat chưa wired.
- Work API là Express 4 + TypeScript + Prisma/PostgreSQL/Neon, JSON API-only tại `127.0.0.1:3002`, JWT Bearer stateless.
- Study Web dev server hiện bind `127.0.0.2:3002`; Study API dùng `127.0.0.1:3003`; Work API dùng `127.0.0.1:3002`.
- Study config hiện lấy default từ static `app/core/constants.py`; không coi `.env.example` là runtime evidence.

## SOURCE_TRACE

```text
AGENTS.md
-> .agents/AGENTS.md + .agents/context-manifest.json
-> .agents/project/{INDEX,architecture,source-status,conventions,dependencies,contracts,workflows}.md
-> .agents/web-work/{AGENTS,INDEX} + study/{AGENTS,INDEX,architecture,api,tests}.md
-> .agents/server-study/{AGENTS,INDEX,architecture,core,apis,tests}.md
-> .agents/server-work/{AGENTS,INDEX,architecture,core,tests}.md
-> apps/study-client/vite.config.ts
-> apps/study-server/app/core/{config.py,constants.py} + .env.example
-> apps/work-server/src/main.ts
```

## DISCREPANCIES_AND_STATUSES

| Item | Status | Impact |
|---|---|---|
| Context drift | `CONTEXT_STALE` | Validator reports source changes in `server-study`, `server-work`, `web-work` and related scopes; future coding/fix must prioritize current source. |
| Study pytest collection | `DECLARED_NOT_RUNNABLE` | Stale register-test imports block the suite. |
| Study OpenAPI | `NOT_FOUND` | Không suy diễn request/response fields từ Work hoặc design docs. |
| Study -> Work event consumer | `DECLARED_NOT_RUNNABLE` | Schemas tồn tại nhưng consumer chưa wired. |
| Node validator | `DECLARED_NOT_RUNNABLE` | `node` không có; Deno compatibility command đã dùng. |

## CHANGES

- Files changed: chỉ thêm worklog này.
- Source/config/contract/context pages: không thay đổi.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Đọc current source của các file đang mở | Đối chiếu được | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-contracts.mjs` | `Contract validation passed` | `VERIFIED` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Báo `CONTEXT_STALE` ở nhiều scope | `CONTEXT_STALE` |

## HANDOFF

- Context đã nạp và sẵn sàng cho task cụ thể.
- Nếu task tiếp theo sửa code, phải đọc current source và trace caller/callee/side effect/test trước khi chỉnh; không dùng snapshot stale làm bằng chứng runtime.
