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
Admin Bearer principal -> xác thực role Admin/user-management permission -> nhận path user_id -> validate body theo contract đã duyệt -> UPDATE candidate legacy users WHERE id=:user_id RETURNING safe UserProfile fields -> no row: candidate 404 -> validate response mapping -> commit -> 200 DESIGN_RESOURCE_UPDATED
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

- Xác thực Bearer JWT trước khi truy cập user row.
- Principal thiếu/sai/không hợp lệ map theo catalog thành 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có role Admin hoặc quyền user-management map theo catalog thành 403 `DESIGN_ACCESS_DENIED`.
- AC-31 ghi precondition Admin đăng nhập và có quyền quản lý user; exact claim, permission source, tenant boundary và policy chưa được định nghĩa.
- Current `validate_current_user_request` chỉ cho Student; không tái sử dụng nó làm Admin guard.
- Authorization chạy trước lookup/update để không tiết lộ user existence cho caller không được phép.

### 0.2. Thứ tự truy cập

- Chỉ bắt đầu candidate mutation sau khi authentication và authorization thành công.
- Không gọi session revoke hoặc audit service theo suy đoán; AC-31 chỉ nêu session revoke ở API #71.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. user_id

- Nhận `user_id:int64!` theo catalog.
- Minimum, malformed/overflow behavior và domain constraint chưa được nêu; không thêm rule ngoài contract.

### 1.2. Candidate body

- Direct body schema chưa được đặc tả; body fields/requiredness/nullability là `SOURCE_REQUIRED`.
- Candidate fields `full_name`, `phone`, `avatar_url`, `role` được suy ra từ intent #70, reusable UserProfile và API #14 precedent; mỗi field vẫn cần owner xác nhận.
- API #14 hiện trim/nonblank/max-150 cho full_name, max-20/nullable-normalize phone, nullable-normalize avatar_url. Chỉ áp dụng cho #70 nếu contract owner duyệt.
- UserRole values, transition policy, phone/avatar null semantics và PUT replacement behavior chưa có nguồn.
- Catalog khai báo 422 `DESIGN_VALIDATION_ERROR`; detailed field errors chưa được định nghĩa.
- Không nhận `status`, `bio`, email, id hoặc credentials từ body candidate.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Lookup/update result

Không có direct SELECT contract. Candidate `UPDATE ... RETURNING` theo id vừa thực hiện mutation và đồng thời trả safe projection; bảng legacy `users` chỉ là source candidate, live schema chưa xác minh.

### 2.2. Candidate branch

- Một row được trả về: map UserProfile candidate.
- Không có row theo id: 404 `DESIGN_RESOURCE_NOT_FOUND` là status/code trực tiếp; điều kiện row-not-found là candidate mapping.
- Không đọc `password_hash`.

### 2.3. JOIN

N/A trong candidate tối thiểu. Không nối legacy BIGINT users với UUID V1-PILOT relations khi chưa có identity mapping được duyệt.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

### 3.1. Target table

`users` legacy là candidate table theo `infra/postgres/study-server/DB.sql`; live table/schema chưa xác minh.

### 3.2. Conditions

Candidate predicate `id = :user_id`. Điều kiện soft-delete/tenant scope chưa được schema/contract xác nhận.

### 3.3. Items update/insert

Candidate full-replacement mutation chỉ khi owner xác nhận:

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

Đây là `DERIVED CANDIDATE`, không phải current source. Không update `status` (API #71), không persist `bio`, không return `password_hash`. API #14 là precedent cho các profile fields và updated_at, nhưng không cập nhật role.

### 3.4. Parameters

| Parameter | Candidate source | Gap |
|---|---|---|
| `:user_id` | Path `user_id:int64!` (DIRECT) | Malformed/domain rule chưa định nghĩa. |
| `:full_name` | Candidate body `full_name` (DERIVED) | Requiredness và validation cần xác nhận. |
| `:phone` | Candidate body `phone` (DERIVED) | Requiredness, null/omit and clear semantics cần xác nhận. |
| `:avatar_url` | Candidate body `avatar_url` (DERIVED) | URI and null/omit semantics cần xác nhận. |
| `:role` | Candidate body `role` (DERIVED) | Enum values, authorization and transition rules cần xác nhận. |

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

- `RETURNING` có row và response mapping hợp lệ: candidate commit transaction rồi trả 200 `DESIGN_RESOURCE_UPDATED`.
- Không có row: trả 404 `DESIGN_RESOURCE_NOT_FOUND`; no-row condition là `DERIVED`.
- Body validation failure: trả 422 `DESIGN_VALIDATION_ERROR`; detailed rules/error structure chưa được định nghĩa.
- DB, mapping hoặc commit failure: trả 500 `DESIGN_INTERNAL_ERROR`; không trả raw SQL/stack detail.
- Transaction ownership/rollback boundary chưa được xác nhận cho #70; API #14 view là precedent hiện tại, không tự động là implementation contract.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Thành công

Map `RETURNING` safe fields vào `UserProfile`: id, full_name, email, role, avatar_url, phone, status, created_at, updated_at. `bio` không có source trong legacy users/API #14 query; omit/null behavior phải được contract owner xác nhận. Trả exact business code `DESIGN_RESOURCE_UPDATED`.

### 5.2. Lỗi

Giữ đúng catalog error status/code: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`. Error envelope null-vs-empty cần đồng bộ với guideline/current helper trước khi wire.

## Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | Catalog DIRECT | 0.1 | Bearer/JWT; Admin policy SOURCE_REQUIRED | Authorization only | 401/403 | None | Admin guard absent. |
| user_id | Catalog DIRECT | 1.1, 3.2 | int64 required; extra constraints SOURCE_REQUIRED | `WHERE id=:user_id` candidate | no row candidate branch | data.id | Legacy id mapping/live schema unverified. |
| full_name | DERIVED from API #14/profile intent | 1.2, 3.3 | Candidate API #14 rules only if approved | Candidate UPDATE | none | data.full_name | Body and requiredness SOURCE_REQUIRED. |
| phone | DERIVED from API #14/profile intent | 1.2, 3.3 | Candidate nullable max-20 only if approved | Candidate UPDATE | none | data.phone | Null/omit/clear semantics open. |
| avatar_url | DERIVED from API #14/profile intent | 1.2, 3.3 | Candidate nullable normalization only if approved | Candidate UPDATE | none | data.avatar_url | Exact URI/null rules open. |
| role | DERIVED from API name/AC-31 | 1.2, 3.3 | Enum/policy SOURCE_REQUIRED | Candidate UPDATE | role transition questions | data.role | No role policy or enum members. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Update profile/role and return safe projection | `UPDATE ... RETURNING` candidate | Legacy `users` candidate | N/A | Candidate SET fields plus safe returned UserProfile fields | None | `id=:user_id` candidate | N/A | N/A | N/A | updated user row | one row success; zero row → candidate 404; DB/mapping failure → catalog 500. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | UPDATE candidate | Legacy `users` (unverified) | `id=:user_id` candidate | full_name, phone, avatar_url, role, updated_at | Body candidates DERIVED; timestamp server-side candidate | SOURCE_REQUIRED; do not invent audit | This DD; no generated mapping | Transaction/rollback ownership SOURCE_REQUIRED; API #14 precedent only | 404 no row (condition DERIVED), 422 validation, 500 system per direct catalog. |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Direct envelope | Envelope generator | 5.1/5.2 | true/false by outcome | Required | Runtime helper behavior is separate. |
| businessCode | string | Direct catalog | Catalog code | 5.1/5.2 | Exact branch code | Required | No extra code. |
| message | string | Envelope | Message generator | 5.1/5.2 | Safe text | SOURCE_REQUIRED | Exact messages unspecified. |
| data.id | int64 | UserProfile direct type; candidate source | `users.id` | 5.1 | Direct mapping candidate | Required on success | Live schema unverified. |
| data.full_name | string | UserProfile direct type; candidate source | `users.full_name` | 5.1 | Updated value | Required | Body/write mapping candidate. |
| data.email | email | UserProfile direct type; candidate source | `users.email` | 5.1 | Preserve existing value | Required | PII policy/source candidate. |
| data.role | UserRole | UserProfile direct type; candidate source | `users.role` | 5.1 | Updated value | Required | Enum and transition policy open. |
| data.avatar_url | uri? | UserProfile direct type; candidate source | `users.avatar_url` | 5.1 | Direct mapping candidate | Null/omit open | Nullable mapping candidate. |
| data.bio | string? | UserProfile optional field | SOURCE_REQUIRED | 5.1 | Do not fabricate | Null/omit open | No source column/query mapping. |
| data.phone | string? | UserProfile direct type; candidate source | `users.phone` | 5.1 | Direct mapping candidate | Null/omit open | PII/null semantics open. |
| data.status | UserStatus | UserProfile direct type; candidate source | `users.status` | 5.1 | Preserve; not mutated here | Required | Enum values; API #71 owns status update. |
| data.created_at | date-time | UserProfile direct type; candidate source | `users.created_at` | 5.1 | ISO-8601 candidate | Required | Live schema/timezone open. |
| data.updated_at | date-time | UserProfile direct type; candidate source | `users.updated_at` | 5.1 | Candidate server timestamp | Required | Runtime behavior unimplemented. |
| meta | object | Envelope | Envelope generator | 5.1/5.2 | `{}` candidate | Required | Update metadata policy open. |
| traceId | uuid | Envelope/middleware | Request trace generator | 5.1/5.2 | Current correlation id | Required | Exact middleware integration when wired. |

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
