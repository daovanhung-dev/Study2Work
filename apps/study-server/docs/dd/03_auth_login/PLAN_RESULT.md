# PLAN_RESULT — Study API #03

**API:** `POST /api/v1/auth/login` — Xác thực thông tin đăng nhập
**Trạng thái:** `Draft — Needs Confirmation`; package DD đủ artifact, response/token/persistence còn discrepancy
**Output folder:** `apps/study-server/docs/dd/03_auth_login/`

## Cơ sở contract và nguồn

- [Catalog API #03 và schemas](../../../../../docs/lists/list_api.md): public/no Bearer; body `email:email!`, `password:string!`; response `ApiEnvelope<UserProfile>`; HTTP `201 DESIGN_RESOURCE_CREATED`; lỗi `422 DESIGN_VALIDATION_ERROR` và `500 DESIGN_INTERNAL_ERROR`.
- [AC-02 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [diagram AC-02](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio): credential/status checks, access/refresh token, client gọi API #04 `/users/me`, lưu session và điều hướng role. AC ghi success 200, credential failure 401, locked account 403.
- Current source: [router](../../../app/api/v1.py), [API #03 view](../../../app/modules/guest/api_03_auth_login/view.py), [query](../../../app/modules/guest/api_03_auth_login/query.py), [validator](../../../app/modules/guest/api_03_auth_login/validate.py), [auth utility](../../../app/utils/auth.py), [test source](../../../tests/modules/guest/api_03_auth_login/test_auth_login.py). Test source được đọc, không chạy trong task docs.
- [DDL candidate](../../../../../infra/postgres/study-server/DB.sql) có `users` và `refresh_tokens`; đây là repo artifact, không chứng minh schema live.
- [API #04 overview](../04_users_me/02_Overview.md) và [API #04 response](../04_users_me/04_Response.md) dùng Student Bearer contract; current #04 source nhận claims `sub` + `roles` và chỉ cho Student.
- Template: registry-wired `createDD-markdown`, [8 Markdown sheets](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/) và [Study workflow](../../../../../.agents/server-study/workflows/README.md). Study DD là folder Markdown, không yêu cầu ZIP.

## Kết quả theo kế hoạch

| Hạng mục | Kết quả |
|---|---|
| Catalog contract | Giữ method/path, public auth, request, `ApiEnvelope<UserProfile>`, HTTP 201 và đúng error set 422/500. |
| Expected/current | Ghi AC-02 và catalog làm expected; ghi riêng current HTTP 200, token fields, 401/403, DB insert và route refresh chưa có catalog contract. |
| Data mapping | Đổi các khẳng định read-only/TBD sai về current source; map current login INSERT `refresh_tokens`, vẫn đánh dấu DDL là candidate. |
| Connected API | Rà AC-02 handoff tới #04; claim names source `sub`/`roles` khác wording AC `user_id`/`role`; hỏi về lần fetch profile sau khi login đã trả profile. |
| Package | 8 sheet lõi + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. |
| Scope | Chỉ API #03 Markdown và worklog/inventory; không sửa API #04, runtime, tests, schema, catalog, diagram hoặc client. |

## Expected behavior và current source

| Chủ đề | Expected behavior | Current source |
|---|---|---|
| Success | Catalog: HTTP 201 `DESIGN_RESOURCE_CREATED`, `ApiEnvelope<UserProfile>`. | HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; data gồm profile và năm token fields. |
| Authentication error | Catalog chỉ liệt kê 422/500; AC-02 mô tả 401/403. | Sai/không tồn tại user: 401; mọi status khác `ACTIVE`: 403. |
| Session | AC-02 yêu cầu token/session; chi tiết persistence nếu server-managed chưa được chốt. | Access JWT + opaque refresh token; HMAC-SHA256 hash và expiry được ghi vào `refresh_tokens`, commit sau login. |
| Refresh | Catalog/AC-02 không có API refresh riêng. | Router có `POST /api/v1/auth/refresh`, revoke/insert token atomically; giữ source-only và ngoài login contract. |
| Input policy | Catalog chỉ nêu required/type/email format. | Email trim/validate, max 255; password whitespace-only bị từ chối. |
| Profile mapping | `UserProfile` có optional `bio`. | Query/response không có `bio`; password hash không được trả. |

## Tables và side effects

- Current login đọc `users` theo email; `password_hash` chỉ dùng verify.
- Current login ghi `refresh_tokens.user_id`, `token_hash`, `expires_at`, `created_at`; raw refresh token không được lưu ở cột hash.
- Current DDL file là candidate; live database/schema chưa được kiểm tra.
- Current source issue token pair; AC-02 muốn tiếp tục gọi #04 `/users/me`. Profile fetch dư thừa và claim naming cần owner xác nhận.

Các quyết định còn mở được liệt kê tại [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
