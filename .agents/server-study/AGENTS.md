# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: SOURCE_BACKED (16 API v1 paths composed; full Study HTTP/unit suite passes in current tree)
TEST_STATUS: SOURCE_BACKED (276 tests passed in current tree)
BUSINESS_MODULE_STATUS: SOURCE_BACKED (register, verify-email dispatch stub, login, refresh, categories, courses, course search, course detail, curriculum, resource detail, avatar upload, profile update, Mentor course list)
DATABASE_SCHEMA_STATUS: PILOT_DDL_PRESENT / live schema not verified
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
| API DD / tài liệu API | `workflows/README.md` (quy tắc deliverable Study API DD) |
| app startup, response, trace, exception | `core/runtime.md` |
| DB/session/query helper hoặc migration | `core/database-security.md` + `database.md` |
| token/password/security helper | `core/database-security.md` |
| declared route | `apis/declared-routes.md` |
| Ollama helper trong Study | `services/ai.md` |
| module/business feature | `modules/README.md` |
| register account flow | `modules/register-account.md` |
| test/fix regression | `tests.md` |

## Critical rules

1. Chỉ coi route hiện có là runtime-verified khi import chain và HTTP test đã pass. APIs #1–#9, #12–#14 và #46 có source/HTTP tests đã pass trong current tree.
2. Không dựng lại `app.module.auth`, `app.module.ai.log` hoặc bất kỳ package legacy nào từ docs/Git history nếu requirement chưa xác nhận.
3. `app/core/security/*` là reusable helper; API #1 register, API #2 verify-email dispatch stub, API #3 login/refresh, API #5 categories, API #6 courses, API #7 course search, API #08 course detail, API #09 curriculum, API #12 resource detail, API #13 avatar upload, API #14 profile update và API #46 Mentor course list là các business flow có source trong Study.
4. Study DB helper không commit; caller/use-case phải sở hữu transaction khi business module tồn tại.
5. Không invent table/column ngoài requirement/contract: `infra/postgres/02_study_db.sql`
   là checked-in V1-PILOT bootstrap/schema artifact; các migration SQL cũng là
   artifact. Chúng không chứng minh live schema availability hoặc migration
   deployment; live metadata mới xác nhận runtime availability.
6. Trước mọi runtime fix, kiểm tra toàn bộ import chain `main -> api/core` và test collection trong đúng source hiện tại.
7. `models.py` chỉ chứa khai báo model class, field, kiểu, default, cấu hình model và chuyển đổi dữ liệu; không đặt hàm/helper, hằng số độc lập, validation input hay business logic ở đây. Validation input thuộc `validate.py`; helper chuẩn hóa dữ liệu dùng chung nằm trong `app/utils/validate.py`, còn Bearer/JWT/token primitives và guard access-JWT dùng chung nằm trong `app/utils/auth.py`. Mọi API cần xác thực access JWT phải gọi `validate_current_user_request(...)` với `role` tường minh; API #4/#13/#14 dùng `STUDENT`, API #46 dùng `MENTOR`. Không lặp lại luồng Bearer/decode/claims tại module API.
8. Validator theo API trả model/dữ liệu đã chuẩn hóa khi hợp lệ; khi input sai, chỉ trả lỗi bằng `return error_response(...)`. Chỉ tạo module-local `validate.py` khi API có rule input riêng; API #4 dùng guard chung từ `app/utils/auth.py` trực tiếp. Không raise response lỗi, tự dựng error response hoặc truy vấn DB/tạo side effect trong validator. Không dùng built-in `ValueError` trong `app/` hoặc `tests/`: helper dùng chung trả `ErrorDetail`, sentinel hoặc kết quả có dữ liệu lỗi để validator/view ánh xạ qua `error_response(...)` tại HTTP boundary. Chỉ dùng các hàm tạo lỗi HTTP có sẵn trong `app/core/responses.py`; lỗi ngoài HTTP giữ cơ chế lỗi nội bộ và không chuyển thành `JSONResponse`. Không áp dụng rule như `@gmail.com` nếu contract chưa xác nhận.
9. `query.py`, nếu module cần truy vấn SQL, chỉ chứa các câu SQL dưới dạng constants; không khai báo function/class/helper, import hay gọi DB helper, chuẩn bị tham số hoặc thực thi truy vấn. Việc bind tham số và gọi `query_one`/`query_many` thuộc `view.py`. Không tạo `query.py` rỗng cho module không truy cập DB; API #2 hiện dispatch qua provider và không có file này.
10. Không coi `apps/study-server/AGENTS.md` hoặc `apps/study-server/.agent/` là context hợp lệ; canonical context duy nhất nằm dưới `.agents/server-study/`.
11. `view.py` là nơi điều phối luồng chính của API. Mỗi thao tác có ý nghĩa trong handler và helper phải có comment ngắn bằng tiếng Việt giải thích mục đích: validation/early return, query hoặc provider call, nhánh nghiệp vụ/lỗi, rollback/commit, ánh xạ dữ liệu và dựng response. Các câu lệnh liền nhau thuộc cùng một bước có thể dùng chung comment; không cần comment riêng cho phép gán đơn giản. API-facing handler vẫn có comment header ngay trước function theo API/endpoint; helper nội bộ không gắn API header. Comment phải mô tả source hiện tại khi DD có discrepancy. Mọi hàm và method trong source, tests và scripts phải có docstring tiếng Việt nêu mục đích; khi phù hợp, docstring mô tả thêm tham số, giá trị trả về, lỗi và tác dụng phụ.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
