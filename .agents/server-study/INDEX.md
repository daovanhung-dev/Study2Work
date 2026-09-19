# Study Server context index

Source root: `apps/study-server/`

## Load order

```text
.agents/AGENTS.md
→ server-study/AGENTS.md
→ server-study/INDEX.md
→ page đúng task
→ exact source + test/contract liên quan
```

## Task routing

| Task | Page bắt đầu |
|---|---|
| Startup, middleware, trace, exception, response | `core/runtime.md` |
| DB/session/query/migration | `core/database-security.md`, `database.md` |
| Auth/password/token | `core/database-security.md` |
| Declared route | `apis/declared-routes.md` |
| Register/module business flow | `modules/README.md`, `modules/register-account.md` |
| Ollama/external service | `services/ai.md` |
| Test/fix/regression | `tests.md`, `workflows/README.md` |

## Page graph

- `architecture.md` — composition, ownership và runtime boundary.
- `apis/declared-routes.md` — route surface hiện tại.
- `core/runtime.md` — startup, response, trace và exception.
- `core/database-security.md` — database/security primitives.
- `database.md` — schema/migration evidence và discrepancy.
- `modules/README.md` — module index và layer responsibility.
- `modules/register-account.md` — API #1 register source flow.
- `services/ai.md` — Ollama adapter boundary.
- `tests.md` — test status và runnable boundary.
- `workflows/README.md` — coding/fix flow và verification order.

Các page trên phải link về source cụ thể; không coi page design/legacy là
runtime evidence nếu current source mâu thuẫn.
