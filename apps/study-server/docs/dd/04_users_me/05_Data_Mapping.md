---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

### Expected behavior — catalog và AC

- Catalog yêu cầu một Bearer JWT, role Student, `ApiEnvelope<UserProfile>`, success HTTP 200 `DESIGN_RESOURCE_RETRIEVED` và errors 401/403/500.
- AC-02 gọi API #04 sau login để lấy hồ sơ/role/permissions; AC-11 gọi API #04 khi mở hồ sơ và sau khi API #14 cập nhật.
- AC-02 ghi claims `user_id`/`role`; catalog #04 không định nghĩa claim keys. AC-02 có nhắc permissions nhưng không nêu schema hoặc nguồn dữ liệu.
- AC-11/API #14 mô tả các trường `full_name`, `bio`, `phone`, `avatar_url`; schema `UserProfile` chỉ đánh dấu `bio` optional, còn catalog API #14 có notation `avatar_url...:uri!` chưa rõ nghĩa.

### Current source flow

1. Route nhận tối đa một header `Authorization`, Session DB và trace ID; endpoint không có path/query/body.
2. Shared auth helper tách Bearer token, decode access JWT, kiểm tra claims và quyền Student trước DB query.
3. Claim `sub` được parse thành positive numeric user ID; `roles` được kiểm tra là list string và chuẩn hóa uppercase.
4. `CURRENT_USER_PROFILE` đọc đúng một row `users` theo `id=:user_id`; không lọc `status` và không đối chiếu `users.role` với token roles.
5. User không có row được source ánh xạ 401; `SQLAlchemyError` rollback rồi trả 500; lỗi `UserProfile` mapping trả 500.
6. Source map row an toàn thành `UserProfile`, trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; không có DB mutation hay external side effect.

Catalog và AC-02 khác nhau về claim wording; API #03 source hiện cũng đã trả profile trước khi client gọi #04. Giữ khác biệt ở trạng thái mở, không tự sửa contract.

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `Authorization` | `header["Authorization"]` | Required; scheme `Bearer`; token phải hợp lệ | `sub` → `users.id`; `roles` → Student guard | Không map trực tiếp | Catalog không khóa claim keys; AC-02 ghi `user_id`/`role` |

## Query Matrix — current source

| Query ID | Mục đích | Type | Base table | Column get | WHERE | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1.1` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.id` | `u.id = :user_id` | `current_user` | Có row → map profile |
| `Q1.2` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.full_name` | `u.id = :user_id` | `current_user` | Có row → map profile |
| `Q1.3` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.email` | `u.id = :user_id` | `current_user` | Có row → map profile |
| `Q1.4` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.role` | `u.id = :user_id` | `current_user` | Role response lấy từ DB |
| `Q1.5` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.avatar_url` | `u.id = :user_id` | `current_user` | Có thể NULL |
| `Q1.6` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.phone` | `u.id = :user_id` | `current_user` | Có thể NULL |
| `Q1.7` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.status` | `u.id = :user_id` | `current_user` | Trả status; không filter status |
| `Q1.8` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.created_at` | `u.id = :user_id` | `current_user` | Có row → map profile |
| `Q1.9` | Đọc hồ sơ hiện tại | `SELECT` | `users AS u` | `u.updated_at` | `u.id = :user_id` | `current_user` | Có row → map profile |

## Mutation Matrix — current source

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — read-only` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Source chỉ SELECT; không tạo/update/delete record |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Response helper | `4.1/4.2/4.3/4.4` | true only on success | N/A | N/A |
| `businessCode` | `string` | Branch constant | Catalog/source branch | `4.1/4.2/4.3/4.4` | `DESIGN_RESOURCE_RETRIEVED`, `DESIGN_AUTHENTICATION_REQUIRED`, `DESIGN_ACCESS_DENIED`, or `DESIGN_INTERNAL_ERROR` | N/A | N/A |
| `message` | `string` | Branch constant | API #04 view/auth helper | `4.1/4.2/4.3/4.4` | Source messages are listed in `04_Response.md` | N/A | Contract does not fix message text |
| `data.id` | `int64` | Direct DB | `users.id` | `4.1` | Python integer serialized as JSON number | N/A | Physical type/deployed schema unverified |
| `data.full_name` | `string` | Direct DB | `users.full_name` | `4.1` | None | N/A | N/A |
| `data.email` | `email` | Direct DB | `users.email` | `4.1` | None | N/A | N/A |
| `data.role` | `UserRole` | Direct DB | `users.role` | `4.1` | None | N/A | Guard separately checks JWT `roles`; source does not compare them |
| `data.avatar_url` | `uri` | Direct DB | `users.avatar_url` | `4.1` | None | JSON `null` is serialized when source value is None | Current model type is `str \| None` |
| `data.bio` | `string?` | No current source | Not selected by query; absent from model | `4.1` | Omitted | Omit | Catalog field is optional; API #14 current source also ignores bio |
| `data.phone` | `string?` | Direct DB | `users.phone` | `4.1` | None | JSON `null` is serialized when source value is None | Current model type is `str \| None` |
| `data.status` | `UserStatus` | Direct DB | `users.status` | `4.1` | None | Model requires non-null | Current model type is string; source does not enforce enum; checked-in DDL candidate lacks NOT NULL |
| `data.created_at` | `date-time` | Direct DB | `users.created_at` | `4.1` | JSON-encoded ISO-8601 | N/A | Physical type/deployed schema unverified |
| `data.updated_at` | `date-time` | Direct DB | `users.updated_at` | `4.1` | JSON-encoded ISO-8601 | N/A | Physical type/deployed schema unverified |
| `meta` | `object` | Envelope default | `success_response` / `error_response` | `4.1/4.2/4.3/4.4` | `{}` | `{}` for these branches | N/A |
| `traceId` | `uuid` | Request correlation | `get_trace_id(request)` | `4.1/4.2/4.3/4.4` | Validate incoming UUID; generate UUID4 if absent/invalid | N/A | Returned in envelope; focused test checks response header |

## 0. Check quyền

### 0.1. Get request header

- Route nhận `Authorization: Bearer <jwt>`; catalog notation lặp `auth{bearer_jwt!}` được biểu diễn bằng một header duy nhất.
- Thiếu header hoặc sai Bearer scheme được shared helper ánh xạ thành `401 DESIGN_AUTHENTICATION_REQUIRED` trước khi query.
- Trace ID lấy từ `get_trace_id(request)`: UUID hợp lệ từ request state hoặc UUID4 fallback.

### 0.2. Decode token

- `decode_access_token` kiểm tra chữ ký, thuật toán đang cấu hình, issuer, audience, expiry, token type `access` và các claim bắt buộc `sub`, `type`, `jti`, `iat`, `exp`, `iss`, `aud`.
- `validate_access_claims` yêu cầu `sub` là chuỗi số dương, `roles` là list không rỗng gồm các chuỗi không trống; role được strip và đổi uppercase.
- JWT lỗi/expiry hoặc claim không hợp lệ trả 401. Decoder error không mang status 401 được helper ánh xạ sang 500 an toàn.
- Current shape là `sub`/`roles`; AC-02 diagram ghi `user_id`/`role`; catalog #04 không khóa claim naming.

### 0.3. Check role

- Nếu danh sách role không chứa `STUDENT`, trả [06_Error.md](./06_Error.md#error-cases) với `403 DESIGN_ACCESS_DENIED` trước DB lookup.
- Nếu có `STUDENT`, tiếp tục xử lý `2`; helper không kiểm tra role DB hoặc account status.

## 1. Get request data

### 1.1. Request shape

- API không có path parameter, query parameter hoặc request body.
- Không nhận `user_id` từ client; identity lấy từ `sub` của access JWT sau khi validate.

## 2. Get user profile

### 2.1. Query current user

`find_current_user` bind `user_id` vào hằng SQL `CURRENT_USER_PROFILE` và gọi `query_one`; SQL chỉ đọc tối đa một hàng.

| Target table | Column get | Chú thích | Query ID |
|---|---|---|---|
| `users AS u` | `u.id` | User ID | `Q1.1` |
| `users AS u` | `u.full_name` | Full name | `Q1.2` |
| `users AS u` | `u.email` | Email | `Q1.3` |
| `users AS u` | `u.role` | Role đưa vào response | `Q1.4` |
| `users AS u` | `u.avatar_url` | Avatar URL | `Q1.5` |
| `users AS u` | `u.phone` | Phone | `Q1.6` |
| `users AS u` | `u.status` | Account status đưa vào response | `Q1.7` |
| `users AS u` | `u.created_at` | Created time | `Q1.8` |
| `users AS u` | `u.updated_at` | Updated time | `Q1.9` |

### 2.2. WHERE

- `u.id = :user_id`, trong đó `user_id` là integer parse từ JWT `sub`; SQL có `LIMIT 1`.
- Query không đọc `password_hash`, permissions table hoặc bảng profile riêng.
- Query không lọc `users.status` và không yêu cầu `users.role = STUDENT`; cả hai là policy gap, không tự thêm điều kiện.

### 2.3. Check result

- Nếu không tìm thấy row, current view trả `401 DESIGN_AUTHENTICATION_REQUIRED` và không gọi rollback; contract không có 404 nhưng chưa xác định semantics cho subject không còn user.
- Nếu `query_one` ném `SQLAlchemyError`, view gọi `db.rollback()`, log theo trace ID và trả `500 DESIGN_INTERNAL_ERROR` không lộ chi tiết DB.
- Nếu có row, chuyển sang bước `3`.

## 3. Map profile

### 3.1. Map UserProfile

- `UserProfile.model_validate(user)` chỉ nhận `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`; `extra="ignore"` loại trường dư.
- Lỗi `ValidationError` khi map hàng trả `500 DESIGN_INTERNAL_ERROR`; nhánh đọc không có mutation cần rollback.
- `model_dump(mode="json")` tuần tự hóa ngày giờ và giữ `avatar_url`/`phone` là `null` khi giá trị nguồn là None.
- `bio` không được SELECT/model; không thêm giá trị hoặc column giả. Permissions cũng không có trong response model.

## 4. Return response

### 4.1. Thành công

- HTTP `200`, `success = true`, `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- `data` là profile đã map; `meta = {}`; `traceId` là UUID của request.
- Chi tiết field: [04_Response.md](./04_Response.md).

### 4.2. Authentication error

- HTTP `401`, `success = false`, `businessCode = DESIGN_AUTHENTICATION_REQUIRED`, `data = {}`, `meta = {}`.
- Áp dụng cho Bearer/JWT/claim lỗi và nhánh không tìm thấy user hiện tại.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 4.3. Authorization error

- HTTP `403`, `success = false`, `businessCode = DESIGN_ACCESS_DENIED`, `data = {}`, `meta = {}`.
- Áp dụng khi JWT hợp lệ nhưng không có role `STUDENT`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 4.4. System error

- HTTP `500`, `success = false`, `businessCode = DESIGN_INTERNAL_ERROR`, `data = {}`, `meta = {}`.
- Áp dụng cho lỗi decoder/config không phải 401, `SQLAlchemyError` hoặc `UserProfile` mapping failure.
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
