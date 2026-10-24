---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---
# Data Mapping

## Flow xử lý data

### Expected behavior theo catalog và AC-02

Catalog định nghĩa request login public và response `ApiEnvelope<UserProfile>`; không đặc tả bảng hay persistence. AC-02 mô tả kiểm tra credential/status, cấp token/session, rồi client gọi API #04 để đọc profile và điều hướng theo role. Status/error khác catalog được giữ thành discrepancy.

### Current source — chỉ riêng POST /auth/login

1. Chuẩn hóa email (trim, validate, max 255) và từ chối password chỉ có whitespace.
2. Đọc `users` theo email, gồm password hash và profile/status fields.
3. Email không tồn tại hoặc password sai trả 401; mọi status khác `ACTIVE` trả 403.
4. Auth utility phát hành access JWT cùng opaque refresh token; source ghi HMAC-SHA256 hash của refresh token và expiry vào `refresh_tokens`, rồi commit.
5. Trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với profile allowlist cộng năm token fields.

Đây là source behavior, không thay thế contract catalog. `POST /auth/refresh` là route riêng hiện có trong cùng module; không gộp mutation/response của route đó vào luồng login bên trên.

## Request Usage Matrix — current source

| Request field | Source                  | Validate                  | Query usage                           | Response usage                                         | Gap                       |
| ------------- | ----------------------- | ------------------------- | ------------------------------------- | ------------------------------------------------------ | ------------------------- |
| `email`     | `request["email"]`    | Required;`email` format | `users.email` lookup                | Không map từ request trực tiếp; map profile từ DB | N/A                       |
| `password`  | `request["password"]` | Required;`string`       | Verify against`users.password_hash` | Không map vào response                               | Hash algorithm/policy TBD |

## Query Matrix — current source

| Query ID  | Mục đích       | Type       | Base table     | Column get          | WHERE               | Result variable   | Branch                   |
| --------- | ----------------- | ---------- | -------------- | ------------------- | ------------------- | ----------------- | ------------------------ |
| `Q1.1`  | Lookup account    | `SELECT` | `users AS u` | `u.id`            | `u.email = email` | `existing_user` | Found → verify          |
| `Q1.2`  | Lookup account    | `SELECT` | `users AS u` | `u.full_name`     | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.3`  | Lookup account    | `SELECT` | `users AS u` | `u.email`         | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.4`  | Lookup credential | `SELECT` | `users AS u` | `u.password_hash` | `u.email = email` | `existing_user` | Found → password verify |
| `Q1.5`  | Lookup account    | `SELECT` | `users AS u` | `u.role`          | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.6`  | Lookup account    | `SELECT` | `users AS u` | `u.avatar_url`    | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.7`  | Lookup account    | `SELECT` | `users AS u` | `u.phone`         | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.8`  | Lookup status     | `SELECT` | `users AS u` | `u.status`        | `u.email = email` | `existing_user` | Found → status check    |
| `Q1.9`  | Lookup account    | `SELECT` | `users AS u` | `u.created_at`    | `u.email = email` | `existing_user` | Found → profile source  |
| `Q1.10` | Lookup account    | `SELECT` | `users AS u` | `u.updated_at`    | `u.email = email` | `existing_user` | Found → profile source  |

## Expected persistence boundary — catalog

| Mutation ID | Operation            | Target table | Record condition | Fields  | Value sources | Mapping file                | Transaction | Failure behavior                    |
| ----------- | -------------------- | ------------ | ---------------- | ------- | ------------- | --------------------------- | ----------- | ----------------------------------- |
| `M1`      | `UNSPECIFIED` | `N/A`      | `N/A`          | `N/A` | `N/A`       | [07_table.md](./07_table.md) | `UNSPECIFIED` | Catalog không đặc tả persistence; không suy ra read-only |

## Current-source mutation matrix — POST /auth/login

| Mutation ID | Operation | Target table | Record condition | Fields written | Value source | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `INSERT` | `refresh_tokens` | Sau khi credential hợp lệ và token pair được phát hành | `user_id`, `token_hash`, `expires_at`, `created_at` | User ID; HMAC hash và expiry từ auth utility; `CURRENT_TIMESTAMP` | [07_table.md](./07_table.md) | Commit sau insert | SQLAlchemy error rollback, log trace ID và trả 500 |

## Expected side effect matrix — AC-02

| Side effect ID | Operation                  | Target                     | Inputs                          | Data Mapping step | Contract gap                                     |
| -------------- | -------------------------- | -------------------------- | ------------------------------- | ----------------- | ------------------------------------------------ |
| `S1`         | `ISSUE_TOKEN_OR_SESSION` | `Auth/session subsystem` | Authenticated`users` identity | `5.1`           | AC-02 yêu cầu token/session; transport/persistence chưa có trong contract |

### Current-source side effect

Source gọi auth utility để phát hành token pair, trả token cho client và ghi refresh-token hash vào `refresh_tokens`. Hash sử dụng HMAC-SHA256 với pepper cấu hình; token/pepper không được ghi vào DD. Thời hạn lấy từ config. Đây không xác nhận schema live hoặc quyết định retention policy.

## Expected profile contract mapping — catalog

| Response field      | Type          | Source type           | Table/column hoặc generator | Data Mapping step | Transform                     | Null/empty rule      | Gap                       |
| ------------------- | ------------- | --------------------- | ---------------------------- | ----------------- | ----------------------------- | -------------------- | ------------------------- |
| `data.id`         | `int64`     | Direct DB             | `users.id`                 | `6.1`           | BIGSERIAL serialized as int64 | `N/A`              | N/A                       |
| `data.full_name`  | `string`    | Direct DB             | `users.full_name`          | `6.1`           | None                          | `N/A`              | N/A                       |
| `data.email`      | `email`     | Direct DB             | `users.email`              | `6.1`           | None                          | `N/A`              | N/A                       |
| `data.role`       | `string`    | Direct DB             | `users.role`               | `6.1`           | None                          | `N/A`              | Role values TBD           |
| `data.avatar_url` | `uri`       | Direct DB             | `users.avatar_url`         | `6.1`           | None                          | `TBD — null/omit` | N/A                       |
| `data.bio`        | `string`    | Unsupported source    | `N/A — no ERD column`     | `6.1`           | `DISCREPANCY/TBD`           | `TBD — null/omit` | Contract/ERD gap          |
| `data.phone`      | `string`    | Direct DB             | `users.phone`              | `6.1`           | None                          | `TBD — null/omit` | N/A                       |
| `data.status`     | `string`    | Direct DB             | `users.status`             | `6.1`           | None                          | `N/A`              | Status branch discrepancy |
| `data.created_at` | `date-time` | Direct DB             | `users.created_at`         | `6.1`           | None                          | `N/A`              | N/A                       |
| `data.updated_at` | `date-time` | Direct DB             | `users.updated_at`         | `6.1`           | None                          | `N/A`              | N/A                       |
| `success`         | `boolean`   | Branch constant       | Processing result            | `6.1/6.2/6.3`   | `true` only on success      | `N/A`              | N/A                       |
| `businessCode`    | `string`    | Branch constant       | Contract                     | `6.1/6.2/6.3`   | Fixed`DESIGN_*` code        | `N/A`              | N/A                       |
| `message`         | `string`    | Branch message        | Application                  | `6.1/6.2/6.3`   | Fixed by branch               | Text TBD             | N/A                       |
| `meta`            | `object`    | Envelope default      | `N/A`                      | `6.1/6.2/6.3`   | `{}`                        | `{}`               | No operation metadata     |
| `traceId`         | `uuid`      | Correlation generator | `N/A`                      | `6.1/6.2/6.3`   | None                          | `TBD`              | Generator TBD             |

## Current-source response matrix

| Response field | Source | Mapping |
|---|---|---|
| `data.id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at` | `users` query result | Allowlist được dựng bởi `build_auth_payload`. |
| `data.access_token` | Auth utility | Access JWT. |
| `data.refresh_token` | Auth utility | Opaque token trả client; chỉ HMAC hash được persist. |
| `data.token_type`, `expires_in`, `refresh_expires_in` | Auth utility/config | Token metadata hiện tại. |
| `data.bio` | Không có trong query/result builder | Không được trả; catalog field chưa có source mapping. |
| `data.password_hash` | `users.password_hash` chỉ dùng để verify | Không được trả. |

## 0. Check quyền — expected và current

### 0.1. Public endpoint

- API public theo catalog, AC-02 và current route; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check trước login.

## 1. Get request data

### 1.1. Get request header

- `content_type`: lấy từ `header["Content-Type"]`; request dùng `application/json`.
- `authorization`: không có; login là public endpoint.

### 1.2. Get request body

- `email`: lấy từ `request["email"]`.
- `password`: lấy từ `request["password"]`.
- Không nhận token, access_token, session_id hoặc profile fields.

## 2. Validate data input — contract boundary

### 2.1. Validate email

- Expected: nếu `email` thiếu/blank hoặc không đúng type `email`, trả `422 DESIGN_VALIDATION_ERROR`; xem [06_Error.md](./06_Error.md#error-cases).
- Expected contract không đặt min/max hoặc canonicalization. Current source trim và giới hạn 255 ký tự; policy đó chưa được duyệt thành normative contract.

### 2.2. Validate password

- Expected: nếu `password` thiếu/blank hoặc không phải `string`, trả `422 DESIGN_VALIDATION_ERROR`; xem [06_Error.md](./06_Error.md#error-cases).
- Expected contract không đặt min/max hoặc character policy. Current source từ chối password chỉ gồm whitespace; chưa nâng điều kiện đó thành normative policy.

## 3. Query account

### 3.1. Lookup by email

- Target: `users AS u`.
- WHERE: `u.email = email` lấy từ xử lý `1.2`.
- Column get được liệt kê từng row trong Query Matrix `Q1.1`–`Q1.10`.

### 3.2. Check query result

- Nếu không có record: AC-02 và current source trả `401 DESIGN_AUTHENTICATION_REQUIRED`; catalog không khai báo code này. Giữ nhánh là `DISCREPANCY/TBD`, không thêm normative error row.
- Nếu có record: đi tới xử lý `4`.

## 4. Verify credentials and status

### 4.1. Verify password

- Current source gọi `app.core.security.verify_password` để so sánh plaintext `password` với `users.password_hash`; catalog không chỉ định thuật toán.
- Không lưu, log hoặc trả plaintext password/password_hash.
- Nếu sai password: AC-02 và current source trả `401`; catalog không khai báo code này. Giữ nhánh là `DISCREPANCY/TBD`, không tự map sang code khác.

### 4.2. Check account status

- Kiểm tra `users.status` trước khi map profile.
- AC-02 mô tả account bị khóa; current source từ chối mọi status khác `ACTIVE` bằng `403 DESIGN_ACCESS_DENIED`. Catalog không khai báo code này; giữ là `DISCREPANCY/TBD`.
- Nếu credential và status hợp lệ: đi tới xử lý `5`.

## 5. Token/session side effect

### 5.1. Issue token or session

- Expected theo AC-02: phát hành access/refresh token hoặc session; claim mô tả ở mức `user_id`, `role`, expiry. Persistence nếu server-managed chưa được chốt.
- Current source: tạo access JWT với claims `sub`, `type=access`, `roles`, `jti`, `iat`, `exp`, `iss`, `aud`; tạo opaque refresh token và HMAC-SHA256 hash bằng pepper config; expiry lấy từ config.
- Current login ghi `user_id`, `token_hash`, `expires_at`, `created_at` vào `refresh_tokens` rồi commit. SQL error rollback; lỗi phát hành token được xử lý an toàn.
- Nếu side effect nội bộ thất bại và flow không thể hoàn tất: đi tới `6.3`.

## 6. Map response

### 6.1. Thành công theo list_api.md

- `HTTPStatus = 201`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_CREATED"`.
- Map từng field `UserProfile` từ `users`; không map `password` hoặc `password_hash`.
- `data.bio`: giữ `DISCREPANCY/TBD` vì không có column ERD.
- `meta = {}`.
- `traceId`: request correlation/generator; exact source TBD.
- Theo contract catalog, token/session không xuất hiện trong `UserProfile`; current source lại trả thêm năm token fields, xem `6.4`.
- Chi tiết: [04_Response.md](./04_Response.md).

### 6.2. Validation error

- HTTP `422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 6.3. Internal error

- HTTP `500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw DB/hash/session detail.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 6.4. Current-source success response

- HTTP `200`, `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `data` gồm profile allowlist và `access_token`, `refresh_token`, `token_type`, `expires_in`, `refresh_expires_in`.
- Đây là source discrepancy với catalog success `201 DESIGN_RESOURCE_CREATED` và `ApiEnvelope<UserProfile>`; không thay thế contract ở `6.1`.
- Source không trả `password_hash` hoặc `bio`.

---

## Phụ lục đối chiếu nguồn Excel

- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô       | Giá trị nguồn                                                                     | Công thức nguồn |
| ----: | -------- | ------------------------------------------------------------------------------------ | ------------------ |
|     2 | `B2`   | Flow xử lý data                                                                    |                    |
|     4 | `D4`   | 0.                                                                                   |                    |
|     4 | `E4`   | Check quyền                                                                         |                    |
|     5 | `E5`   | ・                                                                                   |                    |
|     5 | `F5`   | Thực hiện check quyền                                                             |                    |
|     6 | `E6`   | ・                                                                                   |                    |
|     6 | `F6`   | Get count khi get data từ …                                                        |                    |
|     7 | `G7`   | Table get                                                                            |                    |
|     7 | `K7`   | :                                                                                    |                    |
|     8 | `G8`   | Conditions                                                                           |                    |
|     8 | `K8`   | :                                                                                    |                    |
|    10 | `E10`  | ・                                                                                   |                    |
|    10 | `F10`  | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |                    |
|    11 | `E11`  | ・                                                                                   |                    |
|    11 | `F11`  | Trường hợp giá trị get được bằng 0, trả về status 2                       |                    |
|    13 | `D13`  | 1.                                                                                   |                    |
|    13 | `E13`  | validate data input                                                                  |                    |
|    14 | `F14`  | refer sheet [４．Error]                                                              |                    |
|    16 | `D16`  | 2.                                                                                   |                    |
|    16 | `E16`  | Get thông tin…                                                                     |                    |
|    18 | `F18`  | Table get                                                                            |                    |
|    18 | `K18`  | Column get                                                                           |                    |
|    18 | `P18`  | Chú thích                                                                          |                    |
|    18 | `U18`  | Remarks                                                                              |                    |
|    29 | `F29`  | Target table / join condition                                                        |                    |
|    30 | `F30`  | Target table                                                                         |                    |
|    30 | `N30`  | Join condition                                                                       |                    |
|    30 | `AL30` | 結合種類                                                                             |                    |
|    31 | `F31`  | txn_ams_t0320 AS a                                                                   |                    |
|    32 | `F32`  | txn_amm_v0002 AS b                                                                   |                    |
|    32 | `N32`  | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001             |                    |
|    32 | `AL32` | LEFT JOIN                                                                            |                    |
|    33 | `F33`  | txn_amm_v0002 AS c                                                                   |                    |
|    33 | `N33`  | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02             |                    |
|    33 | `AL33` | LEFT JOIN                                                                            |                    |
|    35 | `F35`  | ・                                                                                   |                    |
|    35 | `G35`  | Điều kiện get data                                                                |                    |
|    37 | `F37`  | ・                                                                                   |                    |
|    37 | `G37`  | Điều kiện sort                                                                    |                    |
|    41 | `D41`  | 3.                                                                                   |                    |
|    41 | `E41`  | Insert/Update thông tin …                                                          |                    |
|    42 | `E42`  | Update table….                                                                      |                    |
|    43 | `E43`  | ・                                                                                   |                    |
|    43 | `F43`  | Items update                                                                         |                    |
|    44 | `F44`  | ・                                                                                   |                    |
|    44 | `G44`  | Refer sheet [xxxx]                                                                   |                    |
|    45 | `E45`  | ・                                                                                   |                    |
|    45 | `F45`  | Điều kiện get data                                                                |                    |
|    46 | `F46`  | ・                                                                                   |                    |
|    46 | `G46`  | auth_user. id = user hiện tại theo token                                           |                    |
|    48 | `D48`  | 4.                                                                                   |                    |
|    48 | `E48`  | check kết quả execute query                                                        |                    |
|    49 | `E49`  | 1. Thành công                                                                      |                    |
|    50 | `F50`  | HTTPStatus = 200                                                                     |                    |
|    51 | `F51`  | Trả về kết quả status = 1                                                        |                    |
|    52 | `E52`  | 2. Lỗi hệ thống phát sinh                                                        |                    |
|    53 | `F53`  | HTTPStatus = 500                                                                     |                    |
|    54 | `F54`  | Trả về kết quả status = 2                                                        |                    |
|    55 | `E55`  | 3. Validate lỗi                                                                     |                    |
|    56 | `F56`  | HTTPStatus = 400                                                                     |                    |
|    57 | `F57`  | Trả về kết quả status = 2                                                        |                    |
|    58 | `E58`  | 4. Ngoài trường hợp trên                                                        |                    |
|    59 | `F59`  | Trả về kết quả status = 2                                                        |                    |

</details>
