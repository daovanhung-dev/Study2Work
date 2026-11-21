# Study Server agent entry

Source root: `apps/study-server/`

```text
CONTEXT_MODE: DEEP
RUNTIME_STATUS: SOURCE_BACKED (current router wires numbered APIs #01–#98; APIs #99–#103 are absent; role module inventory is in modules/README.md and declared-routes.md)
TEST_STATUS: VERIFIED_API_18_FIX (2026-11-16 full Study suite: 1492 passed, 0 failed, 1 Starlette/httpx deprecation warning; see tests.md)
BUSINESS_MODULE_STATUS: SOURCE_BACKED (register, verify-email dispatch stub, login, refresh, categories, courses, course search, reviews, resource detail, lesson resources/next, quiz detail/attempts/answers, attempt result, assignment detail, avatar upload, upload metadata, profile update, Mentor course list, lecture create/detail, content list/create/update/publish/delete, submission list/detail/grade/feedback, support-request list/detail/reply/resolve, course-student roster, notification dispatch/status, course progress/activity analytics, Admin user listing/detail/update/status/delete, course list/detail/update/status/delete, pending Content queue, Content detail, approval and rejection, Admin lesson listing/detail/update/status/delete, Admin quiz list/create/update/delete/statistics, Admin notification list/create/update/delete/status, reported-discussion queue and discussion detail)
DATABASE_SCHEMA_STATUS: TEMP_BRANCH_SCHEMA_VERIFIED (migrations 002–014; production schema/deployment unverified)
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

1. Current source wires numbered APIs #01–#98; APIs #99–#103 have no route/module in the current Study runtime. The full local suite passed 1492 tests after the API #18 auth fix and dedicated test addition on 2026-11-16. API #16–#45 are present in source; module-specific tests are absent for #16–#17, #19–#20, #31 and #35–#45. API #18 has dedicated HTTP coverage. Preserve the API #10 response projection and API #92–#95 OpenAPI test corrections documented in `tests.md`. The 1326-test and nullable-bind results below are dated historical baselines, not current counts.
   API #11 current source returns every PUBLIC resource ordered by ID as `Resource[]`; a valid course with no matching resources returns `200 []`. API #12 current source returns direct HTTP(S) URLs for PUBLIC resources and requires Student Bearer, ACTIVE enrollment, a published parent course and a 300-second signed URL for PRIVATE resources. Focused APIs #05–#12 fake-source tests pass 119 cases on 2026-11-21, including 27 #11/#12 cases; live DB, deployment and storage remain unverified.
2. Không dựng lại `app.module.auth`, `app.module.ai.log` hoặc bất kỳ package legacy nào từ docs/Git history nếu requirement chưa xác nhận.
3. `app/core/security/*` là reusable helper. API endpoint packages follow actor folders: Guest #01–#03/#05–#12/#15; Student #04/#13–#14/#16–#17/#19–#33/#35–#45; Shared #18/#34; Mentor #46–#67; Admin #68–#98. For the SH-07 notification slice, API #18 uses UUID and owner-only access for Student/Mentor/Admin; generic operation lifecycle/result and non-notification producers remain outside its source implementation. API #34 explicitly accepts Student and Mentor. APIs #63–#64 cover Mentor notification dispatch/status, #65–#67 progress/analytics, #78–#81 Admin Content moderation, #82–#86 Admin lessons, #87–#91 quizzes, #92–#96 notifications and #97–#98 discussions. API #63 accepts text content; recipient/channel encoding, common-course rule, outbox schema and provider behavior retain DERIVED/runtime limits. DD #98 remains Draft/UNWIRED and source-vs-DD discrepancy must remain explicit.
4. Study DB helper không commit; caller/use-case phải sở hữu transaction khi business module tồn tại.
5. Không invent table/column ngoài requirement/contract: `infra/postgres/02_study_db.sql`
   là checked-in V1-PILOT bootstrap/schema artifact; các migration SQL cũng là
   artifact. Chúng không chứng minh live schema availability hoặc migration
   deployment; live metadata mới xác nhận runtime availability.
6. Trước mọi runtime fix, kiểm tra toàn bộ import chain `main -> api/core` và test collection trong đúng source hiện tại.
7. `models.py` chỉ chứa khai báo model class, field, kiểu, default, cấu hình model và chuyển đổi dữ liệu; không đặt hàm/helper, hằng số độc lập, validation input hay business logic ở đây. Validation input thuộc `validate.py`; helper chuẩn hóa dữ liệu dùng chung nằm trong `app/utils/validate.py`, còn Bearer/JWT/token primitives và guard access-JWT dùng chung nằm trong `app/utils/auth.py`. Mọi API cần xác thực access JWT phải gọi `validate_current_user_request(...)` với `role` tường minh; guard nhận một role hoặc sequence role. API #4/#13/#14 dùng `STUDENT`, API #46–#67 dùng `MENTOR`; APIs #68–#98 dùng `ADMIN`, API #34 dùng `("STUDENT", "MENTOR")` rồi gắn role với purpose. Không lặp lại luồng Bearer/decode/claims tại module API.
8. Validator theo API trả model/dữ liệu đã chuẩn hóa khi hợp lệ; khi input sai, chỉ trả lỗi bằng `return error_response(...)`. Chỉ tạo module-local `validate.py` khi API có rule input riêng; API #4 dùng guard chung từ `app/utils/auth.py` trực tiếp. Không raise response lỗi, tự dựng error response hoặc truy vấn DB/tạo side effect trong validator. Không dùng built-in `ValueError` trong `app/` hoặc `tests/`: helper dùng chung trả `ErrorDetail`, sentinel hoặc kết quả có dữ liệu lỗi để validator/view ánh xạ qua `error_response(...)` tại HTTP boundary. Chỉ dùng các hàm tạo lỗi HTTP có sẵn trong `app/core/responses.py`; lỗi ngoài HTTP giữ cơ chế lỗi nội bộ và không chuyển thành `JSONResponse`. Không áp dụng rule như `@gmail.com` nếu contract chưa xác nhận.
9. `query.py`, nếu module cần truy vấn SQL, chỉ chứa các câu SQL dưới dạng constants; không khai báo function/class/helper, import hay gọi DB helper, chuẩn bị tham số hoặc thực thi truy vấn. Việc bind tham số và gọi `query_one`/`query_many` thuộc `view.py`. Không tạo `query.py` rỗng cho module không truy cập DB; API #2 hiện dispatch qua provider và không có file này.
10. Không coi `apps/study-server/AGENTS.md` hoặc `apps/study-server/.agent/` là context hợp lệ; canonical context duy nhất nằm dưới `.agents/server-study/`.
11. `view.py` là nơi điều phối luồng chính của API. Mỗi thao tác có ý nghĩa trong handler và helper phải có comment ngắn bằng tiếng Việt giải thích mục đích: validation/early return, query hoặc provider call, nhánh nghiệp vụ/lỗi, rollback/commit, ánh xạ dữ liệu và dựng response. Các câu lệnh liền nhau thuộc cùng một bước có thể dùng chung comment; không cần comment riêng cho phép gán đơn giản. API-facing handler vẫn có comment header ngay trước function theo API/endpoint; helper nội bộ không gắn API header. Comment phải mô tả source hiện tại khi DD có discrepancy. Mọi hàm và method trong source, tests và scripts phải có docstring tiếng Việt nêu mục đích; khi phù hợp, docstring mô tả thêm tham số, giá trị trả về, lỗi và tác dụng phụ.

Exact status/boundary: `architecture.md`, `tests.md`, project `source-status.md`.
