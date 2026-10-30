---
title: "Data Mapping"
order: 5
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
PUT route -> shared ADMIN JWT guard -> signed-int64 path/body validation -> UPDATE checked-in legacy users by id RETURNING safe UserProfile -> 0 rows: 404 / invalid input: 422 / SQL or mapping/commit failure: rollback + 500 -> commit -> 200 DESIGN_RESOURCE_UPDATED
~~~

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Insert/Update thông tin](#step-3-insertupdate-thong-tin)
- [4. Check kết quả execute query](#step-4-check-ket-qua-query)
- [5. Map response](#step-5-map-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- Shared `validate_current_user_request(..., role="ADMIN")` xác thực Bearer/JWT trước khi path parsing hoặc DB access.
- Thiếu/sai JWT trả 401 `DESIGN_AUTHENTICATION_REQUIRED`; thiếu role ADMIN trả 403 `DESIGN_ACCESS_DENIED`.
- ADMIN claim là fallback theo APIs #68/#69; permission relation, tenant boundary, MFA và account-status lookup không có trong current source.
- Error responses dùng helper hiện hành với `data:null` và trace ID.

### 0.2. Ranh giới mutation

- API #70 chỉ cập nhật `full_name`, `phone`, `avatar_url`, `role`, `updated_at`.
- API #71 sở hữu `status`; API #72 sở hữu delete/anonymization.
- Không thêm audit hoặc revoke refresh/access token; policy và ảnh hưởng token sau role change còn SOURCE_REQUIRED.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. user_id

- Nhận raw path `user_id:int64!` và parse signed-int64.
- Malformed hoặc out-of-range trả 422 `DESIGN_VALIDATION_ERROR` với field `user_id`.
- Signed-int64 hợp lệ nhưng không có user row trả 404 `DESIGN_RESOURCE_NOT_FOUND`.
- ID âm/0 vẫn nằm trong miền int64; legacy BIGSERIAL không có row tương ứng nên UPDATE trả zero rows.

### 1.2. Body fallback — DERIVED

Catalog/diagram không khai báo body. Runtime dùng JSON full-replacement với đúng bốn required keys:

| Field | Runtime rule | Evidence/status |
|---|---|---|
| `full_name` | Required string; trim; reject blank; max 150 characters. | API #14 + legacy `VARCHAR(150)`; DERIVED for #70. |
| `phone` | Required key; string or null; trim; blank becomes null; max 20 characters when string. | API #14 + legacy nullable `VARCHAR(20)`; DERIVED for #70. |
| `avatar_url` | Required key; string or null; trim; blank becomes null; no URL syntax/length validation. | API #14 + legacy nullable TEXT; DERIVED for #70. |
| `role` | Required exact string `STUDENT`, `MENTOR` or `ADMIN`. | Current Study role usage + legacy VARCHAR(20); allowlist/transition policy DERIVED. |

- Extra keys are rejected; `status`, `bio`, `email`, IDs, timestamps and credentials are not writable.
- Pydantic body parsing and API-specific validation failures use 422 `DESIGN_VALIDATION_ERROR`.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. UPDATE RETURNING projection

Không có SELECT trước mutation. Một bound `UPDATE users ... WHERE id=:user_id RETURNING ...` vừa thực hiện thay đổi vừa trả projection để dựng `UserProfile` trong cùng transaction.

### 2.2. Source boundary

- Runtime truy vấn checked-in legacy BIGINT `users` candidate, khớp int64 ID và các field của API #04.
- Không JOIN V1-PILOT UUID identity/profile/role relations; không có identity mapping được xác nhận.
- Live schema, grants, migration/deployment chưa được kiểm tra.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

### 3.1. Target table

`users` trong `infra/postgres/study-server/DB.sql` là local candidate; không thêm migration.

### 3.2. Runtime mutation

~~~sql
UPDATE users
SET full_name = :full_name,
    phone = :phone,
    avatar_url = :avatar_url,
    role = :role,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
RETURNING id, full_name, email, role, avatar_url, phone, status, created_at, updated_at
~~~

### 3.3. Điều kiện và field ownership

- `WHERE id = :user_id` là bound predicate; body không được nối vào SQL text.
- `email`, `status`, `created_at` được giữ nguyên; không cập nhật password hash hoặc bio.
- Không áp dụng status/deleted filter: legacy table hiện không có `deleted_at`; suspended/deleted visibility remains an owner policy question.
- SQL được đặt thành constant trong `query.py`; `view.py` bind parameter, execute, map response, commit/rollback.

### 3.4. Parameters

| Parameter | Source | Target | Status |
|---|---|---|---|
| `:user_id` | raw path `user_id:int64!` | `users.id` | Path DIRECT; legacy mapping DERIVED. |
| `:full_name` | normalized body | `users.full_name` | Body/target mapping DERIVED; API #14 validation reused. |
| `:phone` | normalized body | `users.phone` | Body/target mapping DERIVED; null clears the column. |
| `:avatar_url` | normalized body | `users.avatar_url` | Body/target mapping DERIVED; null clears the column. |
| `:role` | allowlisted body | `users.role` | Body/role allowlist DERIVED; transition policy open. |
| server timestamp | `CURRENT_TIMESTAMP` | `users.updated_at` | API #14 precedent; live type/timezone unverified. |

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

- One valid `RETURNING` row: validate safe projection, commit and return 200 `DESIGN_RESOURCE_UPDATED`.
- Zero rows: rollback and return 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Invalid path/body: return 422 `DESIGN_VALIDATION_ERROR`; no DB mutation is attempted for API-level validator failures.
- Query, invalid projection or commit failure: rollback and return safe 500 `DESIGN_INTERNAL_ERROR`.
- Transaction ownership is in the API view, following the existing API #14 caller-owned Session pattern.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Success

Map only `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at` into API #04 `UserProfile`. The model omits unsupported `bio` and ignores any extra source fields. `avatar_url` and `phone` serialize as JSON null when their database values are null. `password_hash` is never selected or returned.

Success envelope uses `DESIGN_RESOURCE_UPDATED`, safe message, empty `meta`, and current trace ID.

### 5.2. Errors

- 401 → `DESIGN_AUTHENTICATION_REQUIRED`
- 403 → `DESIGN_ACCESS_DENIED`
- 404 → `DESIGN_RESOURCE_NOT_FOUND`
- 422 → `DESIGN_VALIDATION_ERROR`
- 500 → `DESIGN_INTERNAL_ERROR`

Error `data` is JSON null under current `error_response`; no shared helper change is needed.

## Request Usage Matrix

| Request field | Source | Step | Validation | Mutation use | Response use | Status/gap |
|---|---|---|---|---|---|---|
| Authorization | Catalog | 0.1 | Bearer/JWT + ADMIN claim | Access guard | None | Admin permission mapping DERIVED; tenant/MFA open. |
| user_id | Catalog | 1.1, 3.3 | Signed-int64 parse | `WHERE id=:user_id` | `data.id` | Invalid parse 422; no row 404; table mapping DERIVED. |
| full_name | DERIVED body | 1.2, 3.2 | Required, trim, nonblank, max 150 | `users.full_name` | `data.full_name` | API #14 rule reused. |
| phone | DERIVED body | 1.2, 3.2 | Required key, nullable, trim, max 20 | `users.phone` | `data.phone` | Null/blank clears field; PII policy open. |
| avatar_url | DERIVED body | 1.2, 3.2 | Required key, nullable, trim | `users.avatar_url` | `data.avatar_url` | No URL syntax validation; source rule absent. |
| role | DERIVED body | 1.2, 3.2 | Exact allowlist | `users.role` | `data.role` | Current role labels only; transition policy open. |

## Query Matrix

| Query ID | Mục đích | Type | Relation | Set/return columns | WHERE | Result | Branch |
|---|---|---|---|---|---|---|---|
| Q1 | Update user profile/role and return safe UserProfile | UPDATE RETURNING | Legacy `users` candidate | Set full_name/phone/avatar_url/role/updated_at; return safe profile fields | `id=:user_id` | One mapped row or None | Success commit; no row 404; query/projection/commit error 500. |

## Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields | Transaction | Audit/side effect | Failure |
|---|---|---|---|---|---|---|---|
| M1 | UPDATE | legacy `users` candidate | `id=:user_id` | full_name, phone, avatar_url, role, updated_at | View commits after safe mapping; rollback no-row/query/map/commit failure | No audit/session/status/delete side effect | Catalog 404/422/500 as above. |

## Response Source Matrix

| Response field | Type | Runtime source | Transform/null rule | Gap |
|---|---|---|---|---|
| success | boolean | success envelope helper | true on success | Current source-backed. |
| businessCode | string | catalog | exact `DESIGN_RESOURCE_UPDATED` | Direct. |
| message | string | view | safe `User updated.` | Wording implementation detail. |
| data.id | int64 | `users.id` RETURNING | direct | Live schema unverified. |
| data.full_name | string | `users.full_name` RETURNING | normalized updated value | Body mapping DERIVED. |
| data.email | email | `users.email` RETURNING | preserve existing value | PII policy open. |
| data.role | UserRole | `users.role` RETURNING | updated allowlisted value | Enum/transition policy DERIVED/open. |
| data.avatar_url | uri? | `users.avatar_url` RETURNING | null stays null | URI syntax not validated. |
| data.bio | string? | No legacy column/API #04 mapping | Omit | Source gap. |
| data.phone | string? | `users.phone` RETURNING | null stays null | PII policy open. |
| data.status | UserStatus | `users.status` RETURNING | preserve; never mutated | API #71 owns change. |
| data.created_at | date-time | `users.created_at` RETURNING | ISO serialization | Live timestamp type/timezone unverified. |
| data.updated_at | date-time | `users.updated_at` RETURNING | server timestamp | API #14 precedent; live behavior unverified. |
| meta | object | success helper | `{}` | No pagination metadata. |
| traceId | uuid | middleware | request trace ID | Current source-backed. |

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
