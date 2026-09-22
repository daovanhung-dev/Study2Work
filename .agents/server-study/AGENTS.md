# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_IMPORT (13 current routes)
TEST_STATUS: COLLECTION_VERIFIED
BUSINESS_MODULE_STATUS: SOURCE_BACKED (register, verify-email dispatch stub, login, refresh, categories, courses, course search)
DATABASE_SCHEMA_STATUS: SOURCE_REQUIRED / do not infer from design docs
```

Canonical page graph: `INDEX.md`.

Source/context priority:

```text
latest user requirement
→ current source
→ current test/contract/schema evidence
→ this context
→ generic best practice
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
| register account flow | `modules/register-account.md` |
| test/fix regression | `tests.md` |

## Critical rules

1. Chỉ coi route hiện có là runtime-verified khi import chain và HTTP test đã pass; hiện Study import, register, verify-email dispatch, categories, courses, course search và auth login/refresh tests đã pass.
2. Không dựng lại `app.module.auth`, `app.module.ai.log` hoặc bất kỳ package legacy nào từ docs/Git history nếu requirement chưa xác nhận.
3. `app/core/security/*` là reusable helper; API #1 register, API #2 verify-email dispatch stub, API #3 login/refresh, API #5 categories, API #6 courses và API #7 course search là các business flow Study hiện được triển khai/xác minh.
4. Study DB helper không commit; caller/use-case phải sở hữu transaction khi business module tồn tại.
5. Không invent table/column ngoài requirement/contract: `infra/postgres/study-server/DB.sql`
   và migration artifacts là checked-in schema/design evidence, còn live metadata
   mới xác nhận runtime availability; migration chưa được apply live.
6. Trước mọi runtime fix, kiểm tra toàn bộ import chain `main -> api/core` và test collection trong đúng source hiện tại.
7. Trong module, `model.py` giữ basic contract validation; `app/utils/validate.py` chứa các helper normalization thuần dùng chung như `strip_email`; `register_account/validate.py` chỉ định nghĩa special validation thuần/reusable với field, điều kiện và message lỗi rõ ràng. Không query DB hoặc tạo side effect trong các validator; `view.py` gọi special validation trước business check/query. Không áp dụng rule như `@gmail.com` nếu contract chưa xác nhận.
8. Không coi `apps/study-server/AGENTS.md` hoặc `apps/study-server/.agent/` là context hợp lệ; canonical context duy nhất nằm dưới `.agents/server-study/`.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
