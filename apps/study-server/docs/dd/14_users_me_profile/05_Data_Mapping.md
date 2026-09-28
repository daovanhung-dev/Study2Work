---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Request Usage Matrix

| Request field | Source | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| `Authorization` | `header["Authorization"]` | `0.1/0.2` | Bearer JWT validation | Identity scope `users.id = user_id` | `0.3` | Không map trực tiếp | Claim validation follows current API #4 source. |
| `Content-Type` | `header["Content-Type"]` | `1.1` | JSON media type | Chọn JSON parser | `1.2` | Không map trực tiếp | Current API convention; list_api không ghi media type. |
| `X-Trace-Id` | `header["X-Trace-Id"]` | `0.1` | Middleware validation/generation | Correlation only | `6.1/6.2/6.3/6.4/6.5` | `traceId` | Current middleware owns invalid-header fallback. |
| `full_name` | `request["full_name"]` | `1.2/2.1` | Required, string, max 150; blank policy TBD | `users.full_name` | `2.5/4.1` | `data.full_name` | Max 150 is current schema evidence. |
| `bio` | `request["bio"]` | `1.3/2.2` | Required/string per contract | `SOURCE_REQUIRED — no users.bio column` | `2.5/4.1` | `data.bio` | Persistence mapping blocked by schema gap. |
| `phone` | `request["phone"]` | `1.4/2.3` | Required/string; max 20; format TBD | `users.phone` | `2.5/4.1` | `data.phone` | Contract required conflicts with nullable schema. |
| `avatar_url` | `request["avatar_url"]` | `1.5/2.4` | URI and requiredness TBD | `users.avatar_url` | `2.5/4.1` | `data.avatar_url` | Contract literal is `avatar_url...:uri!`. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `Q1` | Load safe profile before/after update | `SELECT` | `users` | `u` | `u.id` | `N/A` | `u.id = :user_id` | `N/A` | `N/A` | `LIMIT 1` | `current_user` | No row follows authentication inconsistency handling. |
| `Q2` | Reload safe profile after committed update | `SELECT` | `users` | `u` | `u.id`, `u.full_name`, `u.email`, `u.role`, `u.avatar_url`, `u.phone`, `u.status`, `u.created_at`, `u.updated_at` | `N/A` | `u.id = :user_id` | `N/A` | `N/A` | `LIMIT 1` | `updated_user` | `bio` is not selectable until source-backed. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| `M1` | `UPDATE` | `users` | `users.id = user_id` from JWT `sub` | `full_name`, `phone`, `avatar_url`, `updated_at` | Request body and `current_timestamp` | `TBD — no audit column/source` | [`07_users_update.md`](./07_users_update.md) | View/use-case owned | `ROLLBACK` and `500 DESIGN_INTERNAL_ERROR` on SQL or mapping failure. |
| `M2` | `UPDATE — blocked field` | `users.bio` | `users.id = user_id` from JWT `sub` | `bio` | `request["bio"]` | `TBD` | [`07_users_update.md`](./07_users_update.md) | `SOURCE_REQUIRED` | Do not emit SQL until schema/contract decision is approved. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Current response helper convention | `6.1/6.2/6.3/6.4/6.5` | `true` on success; `false` on error | `N/A` | `N/A` |
| `businessCode` | `string` | Branch constant | `DESIGN_*` contract code | `6.1/6.2/6.3/6.4/6.5` | Fixed by branch | `N/A` | Codes are design-only, not runtime catalog proof. |
| `message` | `string` | Branch message | Application message | `6.1/6.2/6.3/6.4/6.5` | Fixed by branch | `TBD — message catalog` | Message text is not source-locked. |
| `data.id` | `int64` | Query result | `users.id` | `5.1/6.1` | Direct | Required on success | `N/A` |
| `data.full_name` | `string` | Query result | `users.full_name` | `5.1/6.1` | Direct | Required on success | `N/A` |
| `data.email` | `email` | Query result | `users.email` | `5.1/6.1` | Direct | Required on success | `N/A` |
| `data.role` | `string` | Query result | `users.role` | `5.1/6.1` | Direct | Required on success | `N/A` |
| `data.avatar_url` | `uri` | Query result | `users.avatar_url` | `4.1/5.1/6.1` | Direct | `null` allowed by current schema; contract TBD | URI/requiredness semantics unresolved. |
| `data.bio` | `string` | Unresolved source | `N/A — users.bio absent` | `5.1/6.1` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` or omit only after decision | No DB/response source. |
| `data.phone` | `string` | Query result | `users.phone` | `4.1/5.1/6.1` | Direct | `null` allowed by current schema; contract request required | Contract/schema discrepancy. |
| `data.status` | `string` | Query result | `users.status` | `5.1/6.1` | Direct | Required on success | Not updated by API #14. |
| `data.created_at` | `date-time` | Query result | `users.created_at` | `5.1/6.1` | ISO-8601 | Required on success | Not updated by API #14. |
| `data.updated_at` | `date-time` | Query result | `users.updated_at` | `4.1/5.1/6.1` | ISO-8601 | Required on success | Set by update operation. |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3/6.4/6.5` | `{}` | `{}` | No extra metadata source. |
| `traceId` | `uuid` | Trace context | `X-Trace-Id` middleware | `0.1/6.1/6.2/6.3/6.4/6.5` | Validated or generated UUID | Required in envelope | Current middleware is source-backed. |

## 0. Check quyền

### 0.1. Get request header

- `authorization`: lấy từ `header["Authorization"]`.
- `content_type`: lấy từ `header["Content-Type"]`.
- `trace_id`: lấy từ `header["X-Trace-Id"]` hoặc giá trị được current middleware tạo/chuẩn hóa.
- Không nhận `user_id` từ path, query hoặc request body.

### 0.2. Decode token

- Verify Bearer JWT theo current Study security policy.
- `user_id = int(claim.sub)` theo current API #4 validation.
- `roles = claim.roles` theo current API #4 validation.
- Reject missing, malformed, expired hoặc invalid access token với [06_Error.md](./06_Error.md), error case `1`.

### 0.3. Check role

- Nếu `roles` không chứa `STUDENT`: đi tới [06_Error.md](./06_Error.md), error case `2`, HTTP `403`.
- Nếu `roles` chứa `STUDENT`: tiếp tục xử lý `1`.

## 1. Get request data

### 1.1. Check transport metadata

- `content_type`: kiểm tra request là JSON theo current Study convention.
- Nếu parser không nhận được JSON object: đi tới [06_Error.md](./06_Error.md), error case `7`, HTTP `422`.

### 1.2. Get `full_name`

- `full_name`: lấy từ `request["full_name"]`.

### 1.3. Get `bio`

- `bio`: lấy từ `request["bio"]`.
- Không map `bio` vào SQL khi chưa có `users.bio` source.

### 1.4. Get `phone`

- `phone`: lấy từ `request["phone"]`.

### 1.5. Get `avatar_url`

- `avatar_url`: lấy từ `request["avatar_url"]`.
- Không nhận `storage_key`, `file`, `mime_type` hoặc `user_id`.

## 2. Validate data input

### 2.1. Check `full_name`

- Nếu `full_name` thiếu, `NULL`, không phải string hoặc vượt quá 150 ký tự: đi tới [06_Error.md](./06_Error.md), error case `3`, HTTP `422`.
- Blank/whitespace normalization chưa được contract khóa; không tự thêm rule ngoài source.

### 2.2. Check `bio`

- Nếu `bio` thiếu, `NULL` hoặc không phải string theo contract: đi tới [06_Error.md](./06_Error.md), error case `4`, HTTP `422`.
- Length, blank policy và persistence mapping của `bio` là `SOURCE_REQUIRED`.

### 2.3. Check `phone`

- Nếu `phone` thiếu, `NULL`, không phải string hoặc vượt quá 20 ký tự: đi tới [06_Error.md](./06_Error.md), error case `5`, HTTP `422`.
- Contract yêu cầu field, nhưng current schema cho phép nullable; blank/clear policy cần được xác nhận.

### 2.4. Check `avatar_url`

- Nếu semantics được khóa là required và field thiếu/null: đi tới [06_Error.md](./06_Error.md), error case `6`, HTTP `422`.
- Nếu giá trị không phải URI theo policy được phê duyệt: đi tới [06_Error.md](./06_Error.md), error case `6`, HTTP `422`.
- Không tự xác nhận `avatar_url` requiredness từ ký hiệu literal `avatar_url...:uri!`.

### 2.5. Check current user record

- Thực hiện `Q1` để xác nhận `users.id = user_id` tồn tại và lấy profile source trước update nếu implementation chọn pre-read.
- Nếu không có record: dùng authentication inconsistency mapping `401 DESIGN_AUTHENTICATION_REQUIRED` theo current API #4 pattern; contract API #14 không khai báo `404`.

## 3. Update thông tin

### 3.1. Begin transaction

- Transaction boundary thuộc view/use-case theo Study architecture.
- Không commit trong query helper.

### 3.2. Update source-backed fields

- Target table: `users`.
- Điều kiện: `users.id = user_id` lấy từ `JWT.sub`.
- `users.full_name = full_name` lấy từ xử lý `1.2`.
- `users.phone = phone` lấy từ xử lý `1.4`.
- `users.avatar_url = avatar_url` lấy từ xử lý `1.5`.
- `users.updated_at = current_timestamp`.
- Chi tiết mapping: [07_users_update.md](./07_users_update.md), step `3.2`.

### 3.3. Handle unresolved `bio`

- `bio` là request field hợp lệ theo contract nhưng chưa có physical column source-backed.
- Không thêm `bio` vào `UPDATE users` SQL.
- Không tạo `ALTER TABLE`, migration, shadow field hoặc JSON fallback.
- Giữ API DD ở `PARTIALLY COMPLETED / NEEDS USER DECISION` cho đến khi schema/contract decision được phê duyệt.

### 3.4. Check affected rows

- Nếu affected rows bằng `1`: tiếp tục xử lý `3.5`.
- Nếu affected rows bằng `0`: đi tới [06_Error.md](./06_Error.md), error case `8`, HTTP `401` theo current API #4 missing-user convention.
- Nếu database trả lỗi: ROLLBACK và đi tới error case `9`, HTTP `500`.

### 3.5. Commit

- Nếu mutation source-backed thành công: COMMIT.
- Nếu commit thất bại: ROLLBACK và đi tới error case `9`, HTTP `500`.

## 4. Reload profile

### 4.1. Execute `Q2`

- SELECT safe profile fields từ `users` theo `users.id = user_id`.
- Không SELECT `password_hash`.
- `bio` không được SELECT vì current schema không có column source-backed.

### 4.2. Check mapping result

- Nếu `updated_user` không tồn tại sau commit: đi tới error case `9`, HTTP `500` vì response source không nhất quán.
- Nếu profile shape không map được `UserProfile`: đi tới error case `9`, HTTP `500`.

## 5. Map response

### 5.1. Map safe UserProfile

- `data.id = updated_user.id`.
- `data.full_name = updated_user.full_name`.
- `data.email = updated_user.email`.
- `data.role = updated_user.role`.
- `data.avatar_url = updated_user.avatar_url`.
- `data.phone = updated_user.phone`.
- `data.status = updated_user.status`.
- `data.created_at = updated_user.created_at`.
- `data.updated_at = updated_user.updated_at`.
- `data.bio` giữ `SOURCE_REQUIRED`; không tự gán hoặc lấy từ request nếu chưa có persistence contract.

## 6. Trả về response

### 6.1. Success

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_UPDATED`.
- `data = UserProfile` theo [04_Response.md](./04_Response.md).
- `meta = {}`.
- `traceId = trace_id`.

### 6.2. Authentication error

- `HTTPStatus = 401`.
- `success = false`.
- `businessCode = DESIGN_AUTHENTICATION_REQUIRED`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md), error case `1` hoặc `8`.

### 6.3. Authorization error

- `HTTPStatus = 403`.
- `success = false`.
- `businessCode = DESIGN_ACCESS_DENIED`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md), error case `2`.

### 6.4. Validation error

- `HTTPStatus = 422`.
- `success = false`.
- `businessCode = DESIGN_VALIDATION_ERROR`.
- `data = {}`.
- `meta.fieldErrors` chứa field error nếu response contract được triển khai theo current Study envelope.
- Chi tiết: [06_Error.md](./06_Error.md), error case `3` đến `7`.

### 6.5. System error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = DESIGN_INTERNAL_ERROR`.
- `data = {}`.
- ROLLBACK nếu transaction đã bắt đầu và không trả raw SQL/stack trace.
- Chi tiết: [06_Error.md](./06_Error.md), error case `9`.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Sheet logic: `3. Data mapping`.

