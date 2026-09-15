# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED (current routes)
BUSINESS_MODULE_STATUS: VERIFIED (API #1 register only)
DATABASE_SCHEMA_STATUS: VERIFIED (DB.sql applied to 5 non-public schemas; public unchanged)
```

## Load theo task

| Task | Context phải đọc trước source |
|---|---|
| app startup, response, trace, exception | `core/runtime.md` |
| DB/session/query helper hoặc migration | `core/database-security.md` + `database.md` |
| token/password/security helper | `core/database-security.md` |
| declared route | `apis/declared-routes.md` |
| Ollama helper trong Study | `services/ai.md` |
| module/business feature | `modules/README.md` |
| test/fix regression | `tests.md` |

## Critical rules

1. Chỉ coi route hiện có là runnable khi import chain và HTTP test đã pass.
2. Không dựng lại `app.module.auth` hoặc AI log module từ legacy docs/Git history nếu requirement chưa xác nhận.
3. `app/core/security/*` là reusable helper; API #1 là business flow duy nhất đã được triển khai/xác minh.
4. Study DB helper không commit; caller/use-case phải sở hữu transaction khi business module tồn tại.
5. Không invent table/column: `infra/postgres/study-server/DB.sql` và live metadata là schema evidence; migration directory vẫn chưa tồn tại.
6. Trước mọi runtime fix, kiểm tra toàn bộ import chain `main -> api/core` vì hiện có nhiều blocker độc lập.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
