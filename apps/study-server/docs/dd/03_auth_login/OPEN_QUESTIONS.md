# OPEN_QUESTIONS — Study API #03

**Trạng thái:** `Draft — Needs Confirmation`
**Endpoint:** `POST /api/v1/auth/login`

## Q-03-01 — Success status và response schema nào là chuẩn?

**Bằng chứng:** Catalog quy định HTTP `201 DESIGN_RESOURCE_CREATED` và `ApiEnvelope<UserProfile>`. AC-02/current source trả HTTP 200; source dùng `DESIGN_RESOURCE_RETRIEVED` và thêm `access_token`, `refresh_token`, `token_type`, `expires_in`, `refresh_expires_in`.

**Ảnh hưởng:** Client contract không thống nhất về status, business code và payload. `UserProfile` không định nghĩa token fields.

**Cần xác nhận:** Chọn approved status/business code và response schema; xác định token fields có thuộc login response và reusable schema hay không. Không tự cập nhật catalog từ source.

## Q-03-02 — Login được phép trả các lỗi authentication nào?

**Bằng chứng:** Catalog chỉ liệt kê `422/500`. AC-02 và current source trả `401 DESIGN_AUTHENTICATION_REQUIRED` cho user không tồn tại/sai password; current source trả `403 DESIGN_ACCESS_DENIED` cho status khác `ACTIVE`.

**Ảnh hưởng:** Consumer chưa có approved error contract cho credential failure, inactive account hoặc cách tránh lộ trạng thái tài khoản.

**Cần xác nhận:** Chốt 401/403 và business codes, message semantics, cùng policy có chủ ý phân biệt locked/disabled hay không. Giữ nguyên normative error set hiện tại đến khi contract được duyệt.

## Q-03-03 — Token, claims, expiry và transport được duyệt ra sao?

**Bằng chứng:** AC-02 mô tả access/refresh token với `user_id`, `role`, expiry ở mức diagram. Current source phát JWT claims `sub`, `type=access`, `roles`, `jti`, `iat`, `exp`, `iss`, `aud`; refresh token là opaque; expiry lấy từ config.

**Ảnh hưởng:** Claim names/role representation và token lifetime giữa diagram, login source và consumer chưa được chốt như contract.

**Cần xác nhận:** Duyệt claims, token type, lifetime, refresh transport và client storage/session lifecycle; đồng bộ với API #04. Không ghi secret, pepper hay token thật vào DD.

## Q-03-04 — Refresh route cần contract/API ID riêng không?

**Bằng chứng:** `app/api/v1.py` có `POST /api/v1/auth/refresh`, cùng marker #03 và cùng module login; catalog/AC-02 không có endpoint row/flow tương ứng. Source rotate refresh-token hash trong transaction.

**Ảnh hưởng:** Route được source triển khai nhưng không có expected API contract, error set hay DD riêng; gộp nó vào login sẽ làm sai endpoint inventory.

**Cần xác nhận:** Bổ sung API ID và contract riêng hay loại route khỏi exposed surface; chốt request/response/errors/rotation semantics. DD #03 hiện chỉ mô tả route refresh như source-only gap.

## Q-03-05 — Email/password validation policy nào là normative?

**Bằng chứng:** Catalog chỉ nêu `email:email!`, `password:string!`. Current validator trim/validate email, max 255 và từ chối password chỉ có whitespace; OpenAPI metadata cũng có giới hạn email.

**Ảnh hưởng:** Whitespace normalization, max length và password blank semantics chưa được contract owner phê duyệt.

**Cần xác nhận:** Chốt normalization/canonicalization, min/max và blank handling, đồng bộ catalog/OpenAPI/source sau duyệt. Không tự suy ra password-strength policy.

## Q-03-06 — Điều kiện account được login là gì?

**Bằng chứng:** AC-02 mô tả locked account; current source từ chối mọi `status != ACTIVE` bằng 403.

**Ảnh hưởng:** Tập status bị chặn và cách phân biệt trạng thái chưa rõ từ contract.

**Cần xác nhận:** Duyệt trạng thái được phép login, mapping 401/403 và message privacy behavior. Không chỉ ghi locked nếu source hiện tại chặn thêm trạng thái khác.

## Q-03-07 — Refresh-token persistence và schema được quản lý thế nào?

**Bằng chứng:** Current login INSERT `user_id`, HMAC-SHA256 `token_hash`, `expires_at`, `created_at` vào `refresh_tokens`; refresh source revoke/insert atomically. `infra/postgres/study-server/DB.sql` có candidate DDL, nhưng live schema chưa được kiểm tra.

**Ảnh hưởng:** Contract chưa chốt session persistence, retention/cleanup, revoke/logout semantics hay deployed table.

**Cần xác nhận:** Duyệt persistence, rotation/revocation, expiry cleanup, uniqueness/index/FK và schema migration/deployment. Không xem DDL file là live schema evidence.

## Q-03-08 — `UserProfile.bio` được map ở đâu?

**Bằng chứng:** Reusable catalog `UserProfile` có optional `bio`; current login query/response và DDL candidate `users` không có `bio` field.

**Ảnh hưởng:** Contract profile field không được current login source cung cấp.

**Cần xác nhận:** Bổ sung nguồn/schema hoặc điều chỉnh approved profile contract; xác định null/omit behavior. Không tạo giá trị hoặc cột giả trong DD.

## Q-03-09 — AC-02 có cần gọi API #04 sau login không?

**Bằng chứng:** AC-02 yêu cầu tiếp tục `GET /api/v1/users/me` để lấy profile/role/permissions. Current API #03 response đã có profile cơ bản; current #04 đọc JWT `sub` + `roles`, chỉ cho Student và đọc lại profile từ `users`.

**Ảnh hưởng:** Chưa rõ bước #04 là chủ ý để lấy quyền mới nhất hay lặp profile fetch; wording claims `user_id`/`role` của diagram cũng khác source claim names.

**Cần xác nhận:** Chốt handoff/session flow, fields nguồn của permission/role, role routing và claims chung giữa #03/#04. Macro-review cả hai DD khi API #04 được hoàn thiện; không sửa #04 trong phiên này.
