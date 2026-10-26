---
title: "Data Mapping"
order: 5
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> shared ADMIN JWT guard -> parse signed-int64 path/body -> SELECT users.status FOR UPDATE -> no row: 404; unsupported current state: 422 -> UPDATE legacy candidate users.status/updated_at RETURNING safe UserProfile -> nếu target SUSPENDED: revoke refresh_tokens chưa revoke và chưa hết hạn -> validate profile -> commit -> 200 DESIGN_RESOURCE_UPDATED; bất kỳ lỗi DB/mapping/commit nào rollback và map 500
~~~

## Mục lục

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

- Shared `validate_current_user_request(..., role="ADMIN")` xác thực Bearer/JWT và role trước DB access.
- Thiếu/sai token trả 401 `DESIGN_AUTHENTICATION_REQUIRED`; role mismatch trả 403 `DESIGN_ACCESS_DENIED`.
- `ADMIN` claim là mapping DERIVED theo API #68–#70; dedicated user-management permission, tenant/MFA policy không có source.
- Không tra user existence trước authentication để tránh lộ tài nguyên.

### 0.2. Transaction ownership

View API #71 sở hữu user row lock, status update, conditional refresh-token revoke và commit/rollback. Core `execute_query`/`query_one` không commit.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `user_id`

- Route nhận raw path và khai báo `user_id:int64` trong OpenAPI.
- Parser chỉ chấp nhận signed-int64; malformed/overflow trả 422 `DESIGN_VALIDATION_ERROR` theo fallback dùng code trực tiếp có trong catalog.

### 1.2. Candidate body/status

- Direct catalog/diagram không có body schema. Runtime yêu cầu strict `{status}`; đây là `DERIVED`.
- Allowlist target là `ACTIVE` và `SUSPENDED`: suy ra từ operation lock/unlock, diagram STATUS, API #3 ACTIVE check và pilot enum gợi ý; không khẳng định complete UserStatus enum cho legacy users.
- Current row chỉ được đổi khi status là ACTIVE/SUSPENDED. Current state khác trả 422 để giữ verification/deletion lifecycle ngoài endpoint.
- Body thiếu/null/extra field/literal khác trả framework 422 qua middleware `DESIGN_CONTRACT_PATHS`.
- Không nhận role/profile fields của #70 hoặc deletion state/control của #72.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q0 — khóa và đọc trạng thái hiện tại

Q0 chạy sau auth/path/body validation, bind `user_id` vào legacy users candidate và dùng `FOR UPDATE` để status hiện tại không đổi giữa transition check và update.

~~~sql
SELECT status
FROM users
WHERE id = :user_id
FOR UPDATE
~~~

Không có row trả 404. Projection status sai kiểu là lỗi dữ liệu nội bộ 500. Status hiện tại ngoài ACTIVE/SUSPENDED trả 422; row lock được rollback trước khi response.

### 2.2. Schema boundary

`users` và `refresh_tokens` là checked-in legacy BIGINT candidates. V1-PILOT identity projection dùng UUID, không JOIN hoặc ghi thay thế các candidate này. Live metadata/deployment chưa xác minh.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

### 3.1. Q1 — đổi account status

~~~sql
UPDATE users
SET status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
RETURNING id, full_name, email, role, avatar_url, phone, status, created_at, updated_at
~~~

Q1 chỉ cập nhật status/time; email, role, profile fields, password, lifecycle metadata không bị sửa. Same-status request vẫn trả 200 và cập nhật timestamp theo fallback DERIVED.

### 3.2. Q2 — thu hồi refresh sessions khi khóa

~~~sql
UPDATE refresh_tokens
SET revoked_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id
  AND revoked_at IS NULL
  AND expires_at > CURRENT_TIMESTAMP
~~~

Q2 chạy cùng transaction khi target status SUSPENDED, kể cả khi current status đã SUSPENDED. Khi target ACTIVE, Q2 không chạy và API không khôi phục token rows đã revoke. Revoke lỗi làm rollback cả Q1. Token hashes không được đọc hoặc trả.

### 3.3. Access JWT boundary

API #3 login/refresh kiểm tra account status ACTIVE; Q2 thu hồi refresh credentials. Shared access-token guard chỉ xác thực claims/roles, không tra user status/revocation. Existing access JWT có thể dùng tới expiry; không có denylist/version mechanism trong phạm vi này.

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

- Q0 no-row → 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Q0 status không phải string là projection failure → rollback/500; status string ngoài ACTIVE/SUSPENDED → rollback/422 `DESIGN_VALIDATION_ERROR`.
- Q1 no-row → rollback/404; response mapping sai → rollback/500.
- Q2 chỉ chạy với target SUSPENDED; query/revoke/commit failure rollback user mutation và trả safe 500 `DESIGN_INTERNAL_ERROR`.
- Q1/Q2 hoàn tất và safe profile hợp lệ → commit rồi trả 200 `DESIGN_RESOURCE_UPDATED`.
- Không thêm 409 hoặc business code ngoài catalog.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Thành công

Map `id`, `full_name`, `email`, `role`, nullable `avatar_url`, nullable `phone`, `status`, `created_at`, `updated_at` qua API #04 `UserProfile`. `bio` không có source mapping/model field nên omit. Không trả `password_hash`, `token_hash` hoặc token.

### 5.2. Error envelope

Dùng `error_response(...)`: `data:null`, `meta.fieldErrors` nếu có, và `X-Trace-Id` khớp `traceId`. #71 route template được đăng ký trong middleware.

## Request Usage Matrix

| Input | Source | Rule | Query/bind | Branch | Status |
|---|---|---|---|---|---|
| Authorization | Header (DIRECT) | Shared ADMIN guard | No DB bind | auth/role error early return | 401/403 direct |
| `user_id` | Path (DIRECT) | signed int64; malformed/overflow → 422 | Q0/Q1 `:user_id` | no row → 404 | bounds/error mapping DERIVED |
| `status` | JSON body (DERIVED) | required ACTIVE/SUSPENDED only | Q1 `:status` | SUSPENDED → Q2; ACTIVE does not revoke/restore | contract approval open |
| Current status | Q0 result | Must be ACTIVE/SUSPENDED | `users.status` | unknown lifecycle state → 422 | DERIVED guard |

## Query Matrix

| Query ID | Mục đích | Type | Base relation | Columns | JOIN | WHERE | Result | Branch |
|---|---|---|---|---|---|---|---|---|
| Q0 | Lock/read current state | `SELECT ... FOR UPDATE` | Legacy `users` | `status` | None | `id=:user_id` | current user state | no row 404; invalid state 422 |
| Q1 | Update status and return safe profile | `UPDATE ... RETURNING` | Legacy `users` | `status`, `updated_at`, UserProfile allowlist | None | `id=:user_id` | updated row | 404/no row; mapping error 500 |
| Q2 | Revoke active refresh credentials | Conditional `UPDATE` | Legacy `refresh_tokens` | `revoked_at` | None | `user_id=:user_id`, unrevoked, unexpired | affected rows | only target SUSPENDED; failure rolls back |

## Mutation Matrix

| Mutation ID | Operation | Target | Condition | Fields | Transaction | Failure |
|---|---|---|---|---|---|---|
| M1 | Update account status | legacy `users` candidate | locked row status ACTIVE/SUSPENDED | `status`, `updated_at` | caller-owned view transaction | 422 unsupported current state; 404 absent; 500 DB/mapping |
| M2 | Revoke refresh credentials | legacy `refresh_tokens` candidate | target SUSPENDED; `revoked_at IS NULL`; not expired | `revoked_at` | atomic with M1 | rollback M1 and safe 500 |

## Response Source Matrix

| Field | Type | Source | Transform | Null/omit rule | Evidence boundary |
|---|---|---|---|---|---|
| `success` | boolean | ApiEnvelope | true on commit | Required | direct envelope |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_UPDATED` | Required | direct contract |
| `data.id` | int64 | `users.id` | preserve | Required | legacy candidate |
| `data.full_name` | string | `users.full_name` | preserve | Required | API #04 safe model |
| `data.email` | email | `users.email` | preserve | Required | PII policy open |
| `data.role` | string | `users.role` | preserve | Required | not changed by #71 |
| `data.avatar_url` | string? | `users.avatar_url` | preserve | null preserved | API #04 safe model |
| `data.phone` | string? | `users.phone` | preserve | null preserved | API #04 safe model |
| `data.status` | string/UserStatus | `users.status` | target ACTIVE/SUSPENDED | Required | allowlist DERIVED |
| `data.created_at` | date-time | `users.created_at` | ISO serialization | Required | legacy candidate |
| `data.updated_at` | date-time | `users.updated_at` | server timestamp | Required | updated on each accepted call |
| `meta` | object | envelope | `{}` | Empty object | current success helper |
| `traceId` | uuid | middleware | propagate | Required; response header too | current runtime |

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
