# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: DECLARED_NOT_RUNNABLE
BUSINESS_MODULE_STATUS: NOT_FOUND
DATABASE_SCHEMA_STATUS: NOT_FOUND
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

1. Không coi route trong `app/api/v1.py` là runnable chỉ vì decorator tồn tại.
2. Không dựng lại `app.module.auth` hoặc AI log module từ legacy docs/Git history nếu requirement chưa xác nhận.
3. `app/core/security/*` là reusable helper hiện hữu; nó không chứng minh register/login/refresh business flow hiện hữu.
4. Study DB helper không commit; caller/use-case phải sở hữu transaction khi business module tồn tại.
5. Không invent table/column: current schema/migration source là `NOT_FOUND`.
6. Trước mọi runtime fix, kiểm tra toàn bộ import chain `main -> api/core` vì hiện có nhiều blocker độc lập.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
