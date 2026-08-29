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

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `Authorization` | `header["Authorization"]` | Required; `Bearer <jwt>` | Decode `user_id` and `role` claims | Không map trực tiếp | JWT signature/expiry/claim policy TBD |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Column get | WHERE | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1.1` | Read current user | `SELECT` | `users AS u` | `u.id` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.2` | Read current user | `SELECT` | `users AS u` | `u.full_name` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.3` | Read current user | `SELECT` | `users AS u` | `u.email` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.4` | Read current user | `SELECT` | `users AS u` | `u.role` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.5` | Read current user | `SELECT` | `users AS u` | `u.avatar_url` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.6` | Read current user | `SELECT` | `users AS u` | `u.phone` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.7` | Read current user | `SELECT` | `users AS u` | `u.status` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.8` | Read current user | `SELECT` | `users AS u` | `u.created_at` | `u.id = user_id` | `current_user` | Found → map profile |
| `Q1.9` | Read current user | `SELECT` | `users AS u` | `u.updated_at` | `u.id = user_id` | `current_user` | Found → map profile |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete DB record |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `4.1/4.2/4.3/4.4` | `true` only on success | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `4.1/4.2/4.3/4.4` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `4.1/4.2/4.3/4.4` | Fixed by branch | Text TBD | N/A |
| `data.id` | `int64` | Direct DB | `users.id` | `4.1` | BIGSERIAL serialized as int64 | `N/A` | N/A |
| `data.full_name` | `string` | Direct DB | `users.full_name` | `4.1` | None | `N/A` | N/A |
| `data.email` | `email` | Direct DB | `users.email` | `4.1` | None | `N/A` | N/A |
| `data.role` | `string` | Direct DB | `users.role` | `4.1` | None | `N/A` | Role values not enumerated |
| `data.avatar_url` | `uri` | Direct DB | `users.avatar_url` | `4.1` | None | `TBD — null/omit` | N/A |
| `data.bio` | `string` | Unsupported source | `N/A — no ERD column` | `4.1` | `DISCREPANCY/TBD` | Omit when no source | Contract/ERD gap |
| `data.phone` | `string` | Direct DB | `users.phone` | `4.1` | None | `TBD — null/omit` | N/A |
| `data.status` | `string` | Direct DB | `users.status` | `4.1` | None | `N/A` | N/A |
| `data.created_at` | `date-time` | Direct DB | `users.created_at` | `4.1` | None | `N/A` | N/A |
| `data.updated_at` | `date-time` | Direct DB | `users.updated_at` | `4.1` | None | `N/A` | N/A |
| `meta` | `object` | Envelope default | `N/A` | `4.1/4.2/4.3/4.4` | `{}` | `{}` | No pagination/operation metadata |
| `traceId` | `uuid` | Correlation generator | `N/A` | `4.1/4.2/4.3/4.4` | None | `TBD` | Generator TBD |

## 0. Check quyền

### 0.1. Get request header

- `authorization`: lấy từ `header["Authorization"]`.
- Source có notation `auth{bearer_jwt!}` lặp hai lần; runtime contract chuẩn hóa thành một header bắt buộc.

### 0.2. Decode token

- Verify Bearer JWT signature và expiry theo cơ chế auth được phê duyệt.
- `user_id = claim.user_id`.
- `role = claim.role`.

### 0.3. Check role

- Nếu token thiếu, sai hoặc không decode được, trả [06_Error.md](./06_Error.md#error-cases) với `401 DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu token hợp lệ nhưng `role != Student`, trả [06_Error.md](./06_Error.md#error-cases) với `403 DESIGN_ACCESS_DENIED`.
- Nếu có token hợp lệ và role Student, tiếp tục xử lý `2`.

## 1. Get request data

### 1.1. Request shape

- API không có path parameter, query parameter hoặc request body.
- Không nhận `user_id` từ client; chỉ dùng `claim.user_id`.

## 2. Get user profile

### 2.1. Query current user

**Target table**

- `users AS u`.

**Column get**

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `users AS u` | `u.id` | User ID | `Q1.1` |
| `↑` | `u.full_name` | Full name | `Q1.2` |
| `↑` | `u.email` | Email | `Q1.3` |
| `↑` | `u.role` | Role | `Q1.4` |
| `↑` | `u.avatar_url` | Avatar URL | `Q1.5` |
| `↑` | `u.phone` | Phone | `Q1.6` |
| `↑` | `u.status` | Account status | `Q1.7` |
| `↑` | `u.created_at` | Created time | `Q1.8` |
| `↑` | `u.updated_at` | Updated time | `Q1.9` |

### 2.2. WHERE

- `u.id = user_id` lấy từ JWT claim ở xử lý `0.2`.
- Không query `password_hash`, permissions table hoặc profile table chưa được ERD xác nhận.

### 2.3. Check result

- Nếu `current_user` không tồn tại: trả `401 DESIGN_AUTHENTICATION_REQUIRED` theo assumption design-only; contract không khai báo `404`.
- Nếu query lỗi: đi tới `4.4` và trả `500 DESIGN_INTERNAL_ERROR`.
- Nếu có record: tiếp tục xử lý `3`.

## 3. Map profile

### 3.1. Map UserProfile

- Map trực tiếp các column `users` sang `data` theo Response Source Matrix.
- `data.bio`: không có source trong ERD; không tự tạo column/profile table, omit khi không có dữ liệu.
- Không map `password_hash` hoặc raw authentication data.
- Không thêm permissions vào response vì `UserProfile` contract không khai báo field này.

## 4. Return response

### 4.1. Thành công

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `data = UserProfile` mapped từ `users`.
- `meta = {}`.
- `traceId` là request correlation UUID; exact generator TBD.
- Chi tiết: [04_Response.md](./04_Response.md).

### 4.2. Authentication error

- `HTTPStatus = 401`.
- `success = false`.
- `businessCode = "DESIGN_AUTHENTICATION_REQUIRED"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 4.3. Authorization error

- `HTTPStatus = 403`.
- `success = false`.
- `businessCode = "DESIGN_ACCESS_DENIED"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 4.4. System error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw SQL, stack trace, secret hoặc credential detail.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

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
