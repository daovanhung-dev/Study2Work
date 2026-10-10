# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: VERIFIED_IMPORT (13 current routes)
TEST_STATUS: VERIFIED (165 tests)
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
7. `models.py` chỉ chứa khai báo model class, field, kiểu, default, cấu hình model và chuyển đổi dữ liệu; không đặt hàm/helper, hằng số độc lập, validation input hay business logic ở đây. Validation và chuẩn hóa input thuộc `validate.py`; helper thuần dùng chung nằm trong `app/utils/validate.py`.
8. Validator của API #1–#7 trả model/dữ liệu đã chuẩn hóa khi hợp lệ; khi input sai, chỉ trả lỗi bằng `return error_response(...)`. Không raise response lỗi, tự dựng error response hoặc truy vấn DB/tạo side effect trong validator. Helper dùng chung có thể báo lỗi nội bộ bằng exception để validator bắt và ánh xạ qua `error_response(...)`. Không áp dụng rule như `@gmail.com` nếu contract chưa xác nhận.
9. `query.py`, nếu module cần truy vấn SQL, chỉ chứa các câu SQL dưới dạng constants; không khai báo function/class/helper, import hay gọi DB helper, chuẩn bị tham số hoặc thực thi truy vấn. Việc bind tham số và gọi `query_one`/`query_many` thuộc `view.py`. Không tạo `query.py` rỗng cho module không truy cập DB; API #2 hiện dispatch qua provider và không có file này.
10. Không coi `apps/study-server/AGENTS.md` hoặc `apps/study-server/.agent/` là context hợp lệ; canonical context duy nhất nằm dưới `.agents/server-study/`.
11. `view.py` là nơi điều phối luồng chính của API. Mỗi thao tác có ý nghĩa trong handler và helper phải có comment ngắn bằng tiếng Việt giải thích mục đích: validation/early return, query hoặc provider call, nhánh nghiệp vụ/lỗi, rollback/commit, ánh xạ dữ liệu và dựng response. Các câu lệnh liền nhau thuộc cùng một bước có thể dùng chung comment; không cần comment riêng cho phép gán đơn giản. API-facing handler vẫn có comment header ngay trước function theo API/endpoint; helper nội bộ không gắn API header. Comment phải mô tả source hiện tại khi DD có discrepancy. Mọi hàm và method trong source, tests và scripts phải có docstring tiếng Việt nêu mục đích; khi phù hợp, docstring mô tả thêm tham số, giá trị trả về, lỗi và tác dụng phụ.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
