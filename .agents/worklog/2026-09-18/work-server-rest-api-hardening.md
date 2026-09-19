---
task_id: "2026-09-18-work-server-rest-api-hardening"
date: "2026-09-18"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-work"]
cross_scope_dependencies: ["contracts/openapi/work/legacy-web.openapi.json", "apps/work-client/web/src/shared/api/work.ts"]
status: "PARTIAL"
---

# Worklog: Hoàn thiện REST API Work Server và đồng bộ tài liệu

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện đúng 18 route runtime Work Server, giữ nguyên method/path và canonical response envelope; cập nhật security, schema migration, contract, DD và tài liệu liên quan.
- Canonical contract/approved DD: `contracts/openapi/work/legacy-web.openapi.json` và template `createDD-markdown`; target `contracts/openapi/work/openapi.json` vẫn UNWIRED.

## CURRENT_BEHAVIOR

- Source/config: Express router hiện có 18 operation; new/updated passwords dùng bcrypt cost 12, legacy plaintext chỉ còn compatibility fallback; runtime secrets đọc từ environment; public Prisma projections loại `matkhau`.
- Runnable tests: Chưa có server integration suite check-in. Môi trường hiện tại chưa có executable `node`/`npm`; TypeScript/Prisma đã được kiểm tra bằng executable trong `node_modules` chạy qua Deno.
- Runtime wiring: Chỉ `src/routes/api_routes.ts` được mount dưới `/api/v1`; health/tenant/billing/storage/university/interview/webhook target operations chưa wire.

## SOURCE_TRACE

```text
api_routes.ts -> auth middleware/handler -> service -> Prisma schema/migration -> reply/jsonSafe -> legacy OpenAPI + Work Web client + DD
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Runtime route vs target catalog | `api_routes.ts` có 18 route; target `openapi.json` có 57 operation | VERIFIED / EXCLUDED | Không triển khai target operation chưa có source/schema |
| Legacy plaintext accounts | Login runtime kiểm tra bcrypt hoặc fallback plaintext legacy; rehash best-effort | VERIFIED / COMPATIBILITY | Hash account mới; cần policy vận hành để loại bỏ fallback sau migration |
| Secret configuration | `constants.ts` đọc biến môi trường bắt buộc và fail-fast JWT dưới 32 ký tự | VERIFIED / HARDENING | Không ghi secret vào source-backed docs |
| Transaction boundary | Current mutations chưa có explicit transaction | DOCUMENTED / OPEN | Giữ source behavior và nêu trong OPEN_QUESTIONS |

## CHANGES

- Files changed: Work Server source/config/services/routes, Prisma schema/migration/database docs, legacy OpenAPI, README/.env example, seed script/report, DD batch và worklog.
- CONTEXT_UPDATES: Đã cập nhật context page server-work cho env, bcrypt/legacy rehash, safe projection, validation/upload và schema migration.
- Context pages changed: `.agents/server-work/AGENTS.md`, `apis/foundation.md`, `core/auth-config-db.md`, `database.md`, `modules/foundation.md`, `tests.md`.
- Assumptions: Giữ nguyên 18 path runtime; password login chuẩn là `password`, alias `matkhau` chỉ để compatibility.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `corepack pnpm --filter work_server exec tsc --noEmit` | Chưa chạy được vì Node executable không tồn tại | DECLARED_NOT_RUNNABLE |
| `corepack pnpm --filter work_server prisma:validate` | Chưa chạy được vì Node/npm toolchain không tồn tại | DECLARED_NOT_RUNNABLE |
| `deno run --allow-read --allow-env --allow-run scripts/validate-contracts.mjs` | `Contract validation passed.` | VERIFIED |
| `deno run --allow-read --allow-env --allow-run scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK`; skip drift vì source đang có thay đổi chưa commit | VERIFIED_WITH_DRIFT_SKIPPED |
| `deno run ... typescript/lib/tsc.js --noEmit -p apps/work-server/tsconfig.json` | Exit 0 | VERIFIED_FALLBACK |
| `deno run ... prisma/build/index.js validate/generate` | Validate và generate exit 0 với env kiểm thử không production | VERIFIED_FALLBACK |
| DD static validator | 18 folders, 148 Markdown, JSON/link/table/secret checks passed | VERIFIED |
| Work Server integration suite | Không có test runner check-in | NOT_FOUND |

## HANDOFF

- Remaining blockers: Node/npm và database test chưa khả dụng; integration smoke chưa được claim. Cần chạy lại exact `corepack pnpm` commands và login/role/owner/upload smoke khi môi trường runtime sẵn sàng.
- Next owner/action: Review migration/transaction policy và thực hiện integration smoke; hai nhóm target OpenAPI và transaction vẫn là câu hỏi mở.
