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
Admin Bearer principal -> authenticate/authorize role Admin + user-management policy -> nhận path user_id và candidate body status -> validate status theo contract được duyệt -> UPDATE candidate legacy users.status WHERE id=:user_id RETURNING safe UserProfile -> nếu chuyển sang SUSPENDED và policy yêu cầu thì revoke các refresh_tokens còn hiệu lực trong cùng transaction -> map UserProfile -> commit -> 200 DESIGN_RESOURCE_UPDATED; lỗi theo catalog
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

- Xác thực Bearer JWT trước khi đọc/cập nhật account.
- Token thiếu/sai/không hợp lệ map theo catalog sang 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có Admin role hoặc quyền user-management map theo catalog sang 403 `DESIGN_ACCESS_DENIED`.
- AC-31 yêu cầu Admin đăng nhập và có quyền user management; JWT claim, permission source, scope/tenant rule chưa có source.
- Current `validate_current_user_request` chỉ cho Student; không tái sử dụng nó làm Admin guard.
- Authentication/authorization phải hoàn tất trước lookup để không tiết lộ user existence.

### 0.2. Thứ tự truy cập

- Status mutation và conditional session action chỉ bắt đầu sau khi Admin được authorize.
- Không ghi audit/self-lock/last-admin logic vì chưa có contract hoặc schema source.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. user_id

- Nhận path `user_id:int64!` theo catalog.
- Minimum, malformed/overflow behavior và domain constraint chưa được nêu; không invent rule.

### 1.2. Candidate status body

- Body `{status:UserStatus!}` là `DERIVED`; catalog/diagram chưa khai báo request body.
- Candidate values là `ACTIVE` (mở khóa) và `SUSPENDED` (khóa), dựa trên operation và V1-PILOT account_status; không tuyên bố đây là đầy đủ UserStatus enum.
- Legacy `users.status` là VARCHAR; legal value constraint không có trong DDL.
- Catalog khai báo 422 `DESIGN_VALIDATION_ERROR`; invalid/missing status conditions và error details cần được khóa từ contract.
- Không nhận profile/role fields thuộc #70 hoặc delete/anonymize controls thuộc #72.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Update result

Không có direct SELECT contract. Candidate `UPDATE ... RETURNING` theo `user_id` vừa thực hiện mutation và trả safe UserProfile projection; legacy `users` chỉ là schema candidate.

### 2.2. Session rows

API #3 hiện có `refresh_tokens` với `revoked_at`; refresh flow chỉ nhận token chưa revoke, chưa hết hạn và account status ACTIVE. Nếu policy yêu cầu revoke khi khóa, candidate Q2 cập nhật những token rows chưa revoke của user. Không trả token/hash trong response.

### 2.3. JOIN

Candidate query không cần JOIN để map UserProfile hoặc revoke refresh tokens. Không nối legacy BIGINT users với UUID V1-PILOT identity projections.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

### 3.1. Target table

Legacy `users` là candidate table theo `infra/postgres/study-server/DB.sql`; `refresh_tokens` là conditional candidate. Live schema chưa xác minh.

### 3.2. Conditions

Candidate status update dùng `users.id = :user_id`. Chỉ chạy Q2 sau khi Q1 trả user row và target status được xác nhận là `SUSPENDED`.

### 3.3. Items update/insert

Q1 — status update candidate:

~~~sql
UPDATE users
SET status = :status,
    updated_at = CURRENT_TIMESTAMP
WHERE id = :user_id
RETURNING id, full_name, email, role, avatar_url, phone, status, created_at, updated_at
~~~

Q2 — chỉ là candidate khi owner xác nhận cần revoke refresh sessions lúc khóa:

~~~sql
UPDATE refresh_tokens
SET revoked_at = CURRENT_TIMESTAMP
WHERE user_id = :user_id
  AND revoked_at IS NULL
  AND expires_at > CURRENT_TIMESTAMP
~~~

Hai câu SQL trên là `DERIVED CANDIDATE`, không phải current API #71 source. Nếu Q2 được duyệt, chạy cùng transaction với Q1 để không commit status suspend mà bỏ sót refresh-token revoke. Q2 chỉ revoke refresh credentials; existing access JWT vẫn có thể được chấp nhận bởi current stateless JWT guard đến expiry. Không update/restore token rows khi mở khóa.

### 3.4. Parameters

| Parameter | Candidate source | Gap |
|---|---|---|
| `:user_id` | Path `user_id:int64!` (DIRECT) | Malformed/domain rule và live id mapping chưa xác minh. |
| `:status` | Candidate body `status` (DERIVED) | UserStatus members, requiredness/nullability and transition policy SOURCE_REQUIRED. |

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

- Q1 trả một row: map response `UserProfile`; Q2 chỉ chạy theo conditional policy đã duyệt; commit candidate transaction rồi trả 200 `DESIGN_RESOURCE_UPDATED`.
- Q1 không trả row: 404 `DESIGN_RESOURCE_NOT_FOUND`; HTTP/code direct, no-row mapping DERIVED.
- Status body sai theo contract được duyệt: 422 `DESIGN_VALIDATION_ERROR`; exact validation fields/details chưa được nguồn nêu.
- DB/query/mapping/commit failure: rollback candidate transaction rồi trả 500 `DESIGN_INTERNAL_ERROR`; không trả raw SQL/stack trace.
- Không có 409 trong catalog; same-status transition behavior cần xác nhận mà không tự thêm conflict response.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Thành công

Map safe fields `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at` sang `UserProfile`; `status` lấy từ row sau mutation. `bio` không có legacy users/API #4 source; null/omit cần chốt. Không trả password_hash, token hash hoặc refresh token.

### 5.2. Lỗi

Giữ exact catalog codes: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Error envelope `data:null` theo guideline đang khác helper hiện tại `{}`.

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | Catalog DIRECT | 0.1 | Bearer/JWT + Admin policy | Authorize before DB | 401/403 | None | Admin guard/policy absent. |
| user_id | Catalog DIRECT | 1.1, 3.2 | int64 required; other rules SOURCE_REQUIRED | Q1 `WHERE id=:user_id`; Q2 user_id candidate | row/no-row branch | data.id | Live schema/parse behavior open. |
| status | DERIVED from `/status` + AC-31 | 1.2, 3.3 | Candidate ACTIVE/SUSPENDED only; enum contract SOURCE_REQUIRED | Q1 `SET status=:status` | SUSPENDED may trigger Q2 | data.status | Body, legal values and transitions need approval. |
| Request query | Catalog | N/A | None | None | None | None | No query parameters declared. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Update account status and return user profile | `UPDATE ... RETURNING` candidate | Legacy `users` candidate | N/A | SET status/updated_at; return safe UserProfile fields | None | `id=:user_id` | N/A | N/A | N/A | updated user row | one row success; zero row → candidate 404; DB/mapping error → 500. |
| Q2 | Revoke active refresh credentials after suspend if policy requires | `UPDATE` conditional candidate | Legacy `refresh_tokens` | N/A | `revoked_at` | None | `user_id=:user_id AND revoked_at IS NULL AND expires_at>CURRENT_TIMESTAMP` | N/A | N/A | N/A | affected refresh-token rows | only after Q1 row and status SUSPENDED; not access JWT revocation. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | UPDATE status candidate | Legacy `users` (unverified) | `id=:user_id` | status, updated_at | Request candidate `status`; server timestamp candidate | Not specified; do not invent | This DD; no generated mapping | Caller-owned transaction candidate | Zero row → 404 candidate; invalid status → 422; system failure → 500. |
| M2 | Conditional UPDATE/revoke | Legacy `refresh_tokens` (unverified) | `user_id=:user_id AND revoked_at IS NULL` | revoked_at | Server timestamp; only on suspend if owner approves | Not specified | This DD; no generated mapping | Same transaction as M1 if selected | Failure → rollback/500 candidate; has no effect on existing access JWTs. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Direct envelope | Envelope generator | 5.1/5.2 | true/false by outcome | Required | Runtime helper behavior separate. |
| businessCode | string | Direct catalog | Catalog code | 5.1/5.2 | Exact branch code | Required | No extra code. |
| message | string | Envelope | Message generator | 5.1/5.2 | Safe text | SOURCE_REQUIRED | Exact messages unspecified. |
| data.id | int64 | UserProfile direct type; candidate source | `users.id` | 5.1 | Direct mapping candidate | Required on success | Live schema unverified. |
| data.full_name | string | UserProfile direct type; candidate source | `users.full_name` | 5.1 | Preserve existing value | Required | Safe projection candidate. |
| data.email | email | UserProfile direct type; candidate source | `users.email` | 5.1 | Preserve existing value | Required | PII/Admin policy open. |
| data.role | UserRole | UserProfile direct type; candidate source | `users.role` | 5.1 | Preserve existing value | Required | Enum members open; not mutated here. |
| data.avatar_url | uri? | UserProfile direct type; candidate source | `users.avatar_url` | 5.1 | Preserve | Null/omit open | Nullable candidate. |
| data.bio | string? | UserProfile optional field | SOURCE_REQUIRED | 5.1 | Do not fabricate | Null/omit open | No source column/query mapping. |
| data.phone | string? | UserProfile direct type; candidate source | `users.phone` | 5.1 | Preserve | Null/omit open | PII/null semantics open. |
| data.status | UserStatus | UserProfile direct type; candidate source | `users.status` | 5.1 | Updated account status | Required | UserStatus enum and values unconfirmed. |
| data.created_at | date-time | UserProfile direct type; candidate source | `users.created_at` | 5.1 | ISO-8601 candidate | Required | Live schema/timezone open. |
| data.updated_at | date-time | UserProfile direct type; candidate source | `users.updated_at` | 5.1 | Candidate server timestamp | Required | API #71 runtime unimplemented. |
| meta | object | Envelope | Envelope generator | 5.1/5.2 | `{}` candidate | Required | Error null/empty rule discrepancy. |
| traceId | uuid | Envelope/middleware | Request trace generator | 5.1/5.2 | Current correlation ID | Required | Exact integration when wired. |

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
