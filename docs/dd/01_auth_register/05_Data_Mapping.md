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

| Request field | Source | Validate | SQL/mutation usage | Response usage | Gap |
|---|---|---|---|---|---|
| `email` | `request["email"]` | Required; email format | Duplicate lookup; insert `users.email` | `data.email` | N/A |
| `password` | `request["password"]` | Required; approved password policy (threshold TBD) | Hash into `users.password_hash` | Không map vào response | N/A |
| `full_name` | `request["full_name"]` | Required | Insert `users.full_name` | `data.full_name` | N/A |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Column get | WHERE | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Kiểm tra email đã tồn tại | `SELECT` | `users AS u` | `u.id` | `u.email = email` | `existing_user` | `count > 0` → conflict; `count = 0` → continue |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `INSERT` | `users` | N/A — generated primary key | Mỗi column theo mapping | Request, hash, default/generated values | [07_users_insert.md](./07_users_insert.md) | Users insert boundary | `ROLLBACK` và trả 500 khi insert thất bại |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `data.id` | `int64` | Generated DB | `users.id` | `8.1` | Serialize BIGSERIAL as int64 | N/A | N/A |
| `data.full_name` | `string` | Direct DB | `users.full_name` | `8.1` | None | N/A | N/A |
| `data.email` | `email` | Direct DB | `users.email` | `8.1` | None | N/A | N/A |
| `data.role` | `string` | Fixed/input policy | `STUDENT` | `4.1`/`8.1` | Default role | N/A | N/A |
| `data.avatar_url` | `uri` | Direct DB | `users.avatar_url` | `8.1` | None | TBD — null/omit | N/A |
| `data.bio` | `string` | Unsupported source | `N/A — no ERD column` | `8.1` | DISCREPANCY | TBD — null/omit | `DISCREPANCY` |
| `data.phone` | `string` | Direct DB | `users.phone` | `8.1` | None | TBD — null/omit | N/A |
| `data.status` | `string` | DB default | `users.status` | `8.1` | Default `ACTIVE` | N/A | N/A |
| `data.created_at` | `date-time` | DB/application timestamp | `users.created_at` | `8.1` | None | N/A | Generator TBD |
| `data.updated_at` | `date-time` | DB/application timestamp | `users.updated_at` | `8.1` | None | N/A | Generator TBD |
| `traceId` | `uuid` | Request correlation/generator | `N/A` | `8.1/8.2` | None | N/A | Generator TBD |

## 1. Get request data

### 1.1. Get request header

- `content_type`: lấy từ `header["Content-Type"]`.
- `authorization`: không có; API là public và không yêu cầu Bearer token.

### 1.2. Get request body

- `email`: lấy từ `request["email"]`.
- `password`: lấy từ `request["password"]`.
- `full_name`: lấy từ `request["full_name"]`.

## 2. Validate data input

### 2.1. Required

- Nếu `email` là `NULL/BLANK`: trả lỗi [06_Error.md — row 1](./06_Error.md).
- Nếu `password` là `NULL/BLANK`: trả lỗi [06_Error.md — row 2](./06_Error.md).
- Nếu `full_name` là `NULL/BLANK`: trả lỗi [06_Error.md — row 3](./06_Error.md).

### 2.2. Email format

- Nếu `email` không đúng format `email`: trả lỗi [06_Error.md — row 4](./06_Error.md).

### 2.3. Password policy

- Nếu `password` vi phạm password policy đã được phê duyệt: trả lỗi [06_Error.md — row 5](./06_Error.md).
- Min/max và character policy chưa có trong contract; không tự đặt giá trị.

## 3. Check email duplicate

### 3.1. Query existing user

**Target table**

- `users AS u`.

**Column get**

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `users AS u` | `u.id` | Existing user ID | `Q1` |

**WHERE**

- `u.email = email` lấy từ xử lý `1.2`.

### 3.2. Check result

- Nếu `count(existing_user) > 0`: đi tới lỗi [06_Error.md — row 6](./06_Error.md) với HTTP `409`.
- Nếu `count(existing_user) = 0`: đi tới xử lý `4`.

## 4. Prepare account entity

### 4.1. Hash password

- `password_hash = hash(password)`.
- Không lưu `password` plaintext.

### 4.2. Set account defaults

- `role = "STUDENT"` theo AC-01 và API contract.
- `avatar_url = NULL` khi request không cung cấp avatar.
- `phone = NULL` khi request không cung cấp phone.
- `status = "ACTIVE"` theo default của ERD V1.
- `bio`: không tạo mapping vì ERD không có column; xem [02_Overview.md](./02_Overview.md#conflicts).

## 5. BEGIN TRANSACTION

- Boundary transaction là INSERT account vào `users`.
- Không tạo hoặc cập nhật bảng profile riêng vì ERD V1 không xác nhận bảng đó.

## 6. Insert users

### 6.1. Execute insert

- Target table: `users`.
- Items insert: refer [07_users_insert.md](./07_users_insert.md).
- `generated_id`: nhận từ `users.id` sau khi INSERT thành công.

### 6.2. Check insert result

- Nếu INSERT thất bại: `ROLLBACK`; trả lỗi [06_Error.md — row 7](./06_Error.md).
- Nếu INSERT thành công: đi tới xử lý `7`.

## 7. Commit và verification dispatch

### 7.1. COMMIT

- Nếu INSERT `users` thành công: `COMMIT`.
- Sau `COMMIT`, không rollback account chỉ vì verification dispatch cần retry.

### 7.2. Verification dispatch

- Dispatch `POST /api/v1/auth/verify-email/send` với `user_id = generated_id`.
- Dispatch dùng `email` lấy từ xử lý `1.2`.
- API verification trả `202 DESIGN_OPERATION_ACCEPTED` theo contract API #2.
- Email Provider gửi verification email.
- Nếu Email Provider/dispatch thất bại sau `COMMIT`: ghi log và retry; không tạo account thứ hai.

#### 7.2.1. Dispatch parameters

| No | Parameter | Value | Remarks |
|---:|---|---|---|
| 1 | `Content-Type` | `application/json` | Header |
| 2 | `user_id` | `generated_id` từ xử lý `6.1` | Request body |
| 3 | `email` | `email` từ xử lý `1.2` | Request body |

## 8. Map response

### 8.1. Thành công

- `HTTPStatus = 201`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_CREATED"`.
- `message`: message success; nội dung cụ thể TBD.
- `data.id = generated_id`.
- `data.full_name = users.full_name`.
- `data.email = users.email`.
- `data.role = users.role`.
- `data.avatar_url = users.avatar_url`.
- `data.bio`: không có source ERD; giữ gap/TBD, không tự thêm column.
- `data.phone = users.phone`.
- `data.status = users.status`.
- `data.created_at = users.created_at`.
- `data.updated_at = users.updated_at`.
- `meta = {}` khi không có metadata khác.
- `traceId`: request correlation/generator; exact source TBD.
- Không map `password` hoặc `password_hash` vào response.
- Response schema chi tiết: [04_Response.md](./04_Response.md).

## 9. Error handling

### 9.1. Validation error

- HTTP `422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md).

### 9.2. Duplicate email

- HTTP `409`.
- `success = false`.
- `businessCode = "DESIGN_STATE_CONFLICT"`.
- `data = {}`.
- Chi tiết: [06_Error.md — row 6](./06_Error.md).

### 9.3. System/DB error

- Nếu transaction đang active: `ROLLBACK`.
- HTTP `500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw SQL, stack trace, secret hoặc upstream body.
- Chi tiết: [06_Error.md — row 7](./06_Error.md).

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

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
