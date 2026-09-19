---
task_id: "2026-09-18-load-server-work-context"
date: "2026-09-18"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-work"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Nạp context Work Server

## EXPECTED_BEHAVIOR

- Nạp context `server-work` theo registry, sau đó đối chiếu các boundary runtime/API/database/test với source hiện tại.
- Không mở rộng sang Work Web/Mobile khi chưa có dependency thật.

## CURRENT_BEHAVIOR

- Work Server là Express 4 + TypeScript + Prisma/PostgreSQL/Neon, API-only dưới `/api/v1`.
- Auth dùng JWT Bearer stateless; router hiện có auth student/business, student/CV/application và business/JD/application routes.
- Prisma dùng shared client và schema 12 model hiện tại; chưa có server-side session/token denylist.
- Không có test runner/integration suite server được check-in; các source-level TypeScript/Prisma checks là boundary kiểm chứng hiện hành.

## SOURCE_TRACE

```text
.agents/server-work/AGENTS.md
-> .agents/server-work/INDEX.md + architecture/API/core/database/module/test/workflow pages
-> src/app.ts -> src/routes/api_routes.ts
-> auth.middleware.ts -> utils/jwt.ts
-> services/* -> shared Prisma client -> prisma/schema.prisma
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Server test suite | `server-work/tests.md` ghi không có test runner/integration suite được check-in | `NOT_FOUND` | Không tuyên bố API scenarios đã tự động kiểm chứng |
| Legacy/target API contracts | Context xác định `legacy-web.openapi.json` mới là source-aligned; `openapi.json` lớn hơn không được wire | `DISCREPANCY` | API contract task phải dùng route source + legacy contract |
| Legacy services | Một số service tồn tại nhưng không được router import | `UNWIRED` | Không suy diễn runtime behavior từ file tồn tại |

## CHANGES

- Files changed: thêm worklog này; không sửa Work source, route, schema hoặc config.
- CONTEXT_UPDATES: không cập nhật page context vì source/contract không thay đổi.
- Context pages changed: none.
- Assumptions: `context work` được hiểu là scope `server-work`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Read current source: `src/app.ts`, `src/main.ts`, `src/routes/api_routes.ts`, auth/config/Prisma/schema | Route composition và boundaries đối chiếu được | `VERIFIED` |
| `node scripts/validate-agent-context.mjs` | `node` không tồn tại trong shell | `DECLARED_NOT_RUNNABLE` |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_OK (.agents/context-manifest.json)` | `VERIFIED` |

## HANDOFF

- Remaining blockers: chưa chạy TypeScript/Prisma checks vì chưa được yêu cầu và Node toolchain hiện không khả dụng.
- Next owner/action: nếu có task cụ thể, bắt đầu từ page API/module/core tương ứng rồi trace route → middleware → service → Prisma → response.
