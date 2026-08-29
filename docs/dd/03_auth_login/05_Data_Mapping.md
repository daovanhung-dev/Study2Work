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
| `email` | `request["email"]` | Required; `email` format | `users.email` lookup | Không map từ request trực tiếp; map profile từ DB | N/A |
| `password` | `request["password"]` | Required; `string` | Verify against `users.password_hash` | Không map vào response | Hash algorithm/policy TBD |

## Query Matrix

| Query ID | Mục đích | Type | Base table | Column get | WHERE | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1.1` | Lookup account | `SELECT` | `users AS u` | `u.id` | `u.email = email` | `existing_user` | Found → verify |
| `Q1.2` | Lookup account | `SELECT` | `users AS u` | `u.full_name` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.3` | Lookup account | `SELECT` | `users AS u` | `u.email` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.4` | Lookup credential | `SELECT` | `users AS u` | `u.password_hash` | `u.email = email` | `existing_user` | Found → password verify |
| `Q1.5` | Lookup account | `SELECT` | `users AS u` | `u.role` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.6` | Lookup account | `SELECT` | `users AS u` | `u.avatar_url` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.7` | Lookup account | `SELECT` | `users AS u` | `u.phone` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.8` | Lookup status | `SELECT` | `users AS u` | `u.status` | `u.email = email` | `existing_user` | Found → status check |
| `Q1.9` | Lookup account | `SELECT` | `users AS u` | `u.created_at` | `u.email = email` | `existing_user` | Found → profile source |
| `Q1.10` | Lookup account | `SELECT` | `users AS u` | `u.updated_at` | `u.email = email` | `existing_user` | Found → profile source |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete DB record |

## Side Effect Matrix

| Side effect ID | Operation | Target | Inputs | Data Mapping step | Contract gap |
|---|---|---|---|---|---|
| `S1` | `ISSUE_TOKEN_OR_SESSION` | `Auth/session subsystem` | Authenticated `users` identity | `5.1` | Token type, field, transport và persistence TBD |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `data.id` | `int64` | Direct DB | `users.id` | `6.1` | BIGSERIAL serialized as int64 | `N/A` | N/A |
| `data.full_name` | `string` | Direct DB | `users.full_name` | `6.1` | None | `N/A` | N/A |
| `data.email` | `email` | Direct DB | `users.email` | `6.1` | None | `N/A` | N/A |
| `data.role` | `string` | Direct DB | `users.role` | `6.1` | None | `N/A` | Role values TBD |
| `data.avatar_url` | `uri` | Direct DB | `users.avatar_url` | `6.1` | None | `TBD — null/omit` | N/A |
| `data.bio` | `string` | Unsupported source | `N/A — no ERD column` | `6.1` | `DISCREPANCY/TBD` | `TBD — null/omit` | Contract/ERD gap |
| `data.phone` | `string` | Direct DB | `users.phone` | `6.1` | None | `TBD — null/omit` | N/A |
| `data.status` | `string` | Direct DB | `users.status` | `6.1` | None | `N/A` | Status branch discrepancy |
| `data.created_at` | `date-time` | Direct DB | `users.created_at` | `6.1` | None | `N/A` | N/A |
| `data.updated_at` | `date-time` | Direct DB | `users.updated_at` | `6.1` | None | `N/A` | N/A |
| `success` | `boolean` | Branch constant | Processing result | `6.1/6.2/6.3` | `true` only on success | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `6.1/6.2/6.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `6.1/6.2/6.3` | Fixed by branch | Text TBD | N/A |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | `{}` | `{}` | No operation metadata |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | None | `TBD` | Generator TBD |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo list và AC-02; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check trước login.

## 1. Get request data

### 1.1. Get request header

- `content_type`: lấy từ `header["Content-Type"]`; request dùng `application/json`.
- `authorization`: không có; login là public endpoint.

### 1.2. Get request body

- `email`: lấy từ `request["email"]`.
- `password`: lấy từ `request["password"]`.
- Không nhận token, access_token, session_id hoặc profile fields.

## 2. Validate data input

### 2.1. Validate email

- Nếu `email` thiếu/blank hoặc không đúng type `email`: trả `422 DESIGN_VALIDATION_ERROR`, xem [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc canonicalization ngoài type `email`.

### 2.2. Validate password

- Nếu `password` thiếu/blank hoặc không phải `string`: trả `422 DESIGN_VALIDATION_ERROR`, xem [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc character policy.

## 3. Query account

### 3.1. Lookup by email

- Target: `users AS u`.
- WHERE: `u.email = email` lấy từ xử lý `1.2`.
- Column get được liệt kê từng row trong Query Matrix `Q1.1`–`Q1.10`.

### 3.2. Check query result

- Nếu không có record: AC-02 mô tả `401 DESIGN_AUTHENTICATION_REQUIRED`; list_api.md không khai báo code này. Giữ nhánh là `DISCREPANCY/TBD`, không thêm normative error row.
- Nếu có record: đi tới xử lý `4`.

## 4. Verify credentials and status

### 4.1. Verify password

- So sánh plaintext `password` từ request với `users.password_hash` bằng cơ chế hash verify được phê duyệt.
- Không lưu, log hoặc trả plaintext password/password_hash.
- Nếu sai password: AC-02 mô tả `401`; list_api.md không khai báo code này. Giữ nhánh là `DISCREPANCY/TBD`, không tự map sang code khác.

### 4.2. Check account status

- Kiểm tra `users.status` trước khi map profile.
- Nếu account bị khóa: AC-02 mô tả `403 DESIGN_ACCESS_DENIED`; list_api.md không khai báo code này. Giữ nhánh là `DISCREPANCY/TBD`, không tự map sang code khác.
- Nếu credential và status hợp lệ: đi tới xử lý `5`.

## 5. Token/session side effect

### 5.1. Issue token or session

- Sau khi credential/status hợp lệ, kích hoạt token/session issuance theo AC-02.
- Token type, claims, transport, expiry, persistence và response field chưa có source xác nhận; không tự thêm vào DD response.
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
- Token/session không xuất hiện trong response schema V1.
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

