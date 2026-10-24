---
title: "Data Mapping"
order: 5
dd_id: "69"
api_name: "Lấy chi tiết user"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> xác thực role/quyền user management -> nhận path user_id -> Q1 candidate đọc một legacy users row theo id -> không có row: candidate 404 -> map UserProfile safe projection -> trả 200 hoặc exact catalog errors
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

- Xác thực Bearer JWT và kiểm tra role Admin cùng quyền user management trước khi đọc hồ sơ.
- Thiếu hoặc token không hợp lệ map theo catalog sang 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có quyền Admin/user management map theo catalog sang 403 DESIGN_ACCESS_DENIED.
- Current helper validate_current_user_request chỉ cho Student; không dùng helper này làm Admin guard.
- Claim role, permission policy, identity mapping và tenant/scope boundary chưa có source; phải được chốt trước implementation.

### 0.2. Thứ tự truy cập

- Không query user row trước khi hoàn tất authorization.
- Không trả thông tin xác nhận user có tồn tại khi caller chưa được phép truy cập.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. user_id

- Nhận path user_id theo kiểu int64 bắt buộc.
- Không tự thêm minimum, enum, format hoặc validation rule khác catalog.
- Catalog không liệt kê 422; malformed, overflow hoặc ID ngoài miền hỗ trợ cần được contract owner xác nhận trước khi chọn HTTP behavior.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query candidate — legacy users

Query dưới đây chỉ là candidate trên legacy BIGINT schema; không khẳng định relation đó hiện có trong live DB.

~~~sql
SELECT
    u.id,
    u.full_name,
    u.email,
    u.role,
    u.avatar_url,
    u.phone,
    u.status,
    u.created_at,
    u.updated_at
FROM users AS u
WHERE u.id = :user_id
LIMIT 1
~~~

- Bind :user_id từ path; không ghép ID trực tiếp vào SQL.
- Không chọn password_hash.
- Không JOIN V1-PILOT identity_projections, learner_profiles hoặc service-role tables.
- Không có filter status; contract không nói loại trừ suspended, deleted hoặc anonymized user.

### 2.2. Candidate branch

- Nếu Q1 trả một row, map sang UserProfile và trả 200 DESIGN_RESOURCE_RETRIEVED.
- Nếu Q1 không có row, trả 404 DESIGN_RESOURCE_NOT_FOUND. Mapping này là DERIVED theo detail resource contract.
- Nếu query hoặc mapping thất bại, trả 500 DESIGN_INTERNAL_ERROR theo catalog.
- Nếu authorization thất bại, trả 401/403 trước khi thực hiện Q1.

### 2.3. JOIN

Không có JOIN trong candidate. Mọi field candidate nằm trên legacy users. Pilot UUID relations không được nối trực tiếp.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

N/A — API #69 chỉ đọc một hồ sơ; không có INSERT, UPDATE hoặc DELETE.

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

- Kết quả có đúng một row: đi tới bước 5.
- Không có row: candidate 404 DESIGN_RESOURCE_NOT_FOUND.
- Query exception hoặc mapping không hợp lệ: 500 DESIGN_INTERNAL_ERROR.
- Không chuyển lỗi SQL hoặc stack trace ra response.

<a id="step-5-map-response"></a>

## 5. Map response

| Response field | Candidate source | Mapping/null rule | Status |
|---|---|---|---|
| data.id | users.id | BIGINT candidate serialized as int64 | Legacy candidate |
| data.full_name | users.full_name | Direct mapping | Legacy candidate |
| data.email | users.email | Direct mapping; Admin-only PII | Legacy candidate |
| data.role | users.role | Return stored value; do not invent enum conversion | Legacy candidate; enum set unresolved |
| data.avatar_url | users.avatar_url | Preserve source value; null/omit behavior open | Nullable candidate |
| data.bio | No approved source | Do not synthesize; omit only as optional-field proposal | SOURCE_REQUIRED |
| data.phone | users.phone | Preserve source value; null/omit behavior open | Nullable PII candidate |
| data.status | users.status | Return stored value; do not invent enum conversion | Legacy candidate; enum set unresolved |
| data.created_at | users.created_at | Serialize as date-time | Legacy candidate; timezone unresolved |
| data.updated_at | users.updated_at | Serialize as date-time | Legacy candidate; timezone unresolved |
| meta | Envelope convention | Empty object candidate | No pagination |
| traceId | Current middleware | Validated or generated UUID | Current source convention |

Không trả password_hash, token, token hash hoặc credential.

### 5.1. Thành công

- HTTPStatus = 200.
- success = true.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- data = một UserProfile theo contract catalog.
- meta = {} candidate.
- traceId = request trace ID.

### 5.2. Lỗi

Chi tiết HTTP status và businessCode xem [06_Error.md](./06_Error.md). Current error helper dùng data:{} nếu caller không truyền data; API guideline mô tả data:null. API #69 chưa wired nên discrepancy này chưa phải runtime behavior của endpoint.

<a id="request-usage-matrix"></a>

## Request Usage Matrix

| Request item | Used by | Candidate query or response use | Status |
|---|---|---|---|
| Authorization | Step 0 | Authenticate and authorize Admin before Q1 | DIRECT requirement; Admin implementation SOURCE_REQUIRED |
| user_id | Step 1/Q1 | Bound to u.id = :user_id; maps to data.id | Type DIRECT; query candidate |
| Body | None | None | DIRECT |
| Query | None | None | DIRECT |

<a id="query-matrix"></a>

## Query Matrix

| Query | Type | Candidate source | Column | Predicate/condition | Evidence |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy users AS u | id, full_name, email, role, avatar_url, phone, status, created_at, updated_at | u.id = :user_id; LIMIT 1 | Safe projection precedent; legacy candidate, live schema unknown |
| Q1 | Result check | Candidate result | User row | One row → map; no row → 404 | Missing-row mapping DERIVED |
| Q1 | Exclusion | Legacy users | password_hash | Never select or serialize | Security boundary |
| JOIN | N/A | N/A | None | No join | No cross-model identity mapping |
| Q2 | N/A | N/A | No count query | Single detail | Not needed |

<a id="mutation-matrix"></a>

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #69 is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

<a id="response-source-matrix"></a>

## Response Source Matrix

| Response field | Contract type | Candidate source | Mapping/null rule | Evidence status |
|---|---|---|---|---|
| success | boolean | Envelope branch | true on success; false on error | DIRECT convention |
| businessCode | string | Catalog | Exact code per branch | DIRECT |
| message | string | Safe application message | Exact text unspecified | DERIVED |
| data.id | int64 | users.id | Direct candidate mapping | Legacy BIGINT candidate |
| data.full_name | string | users.full_name | Direct candidate mapping | Legacy candidate |
| data.email | email | users.email | Direct candidate mapping; Admin-only PII | Legacy candidate |
| data.role | UserRole | users.role | Preserve stored value | Candidate; enum members unresolved |
| data.avatar_url | uri? | users.avatar_url | Preserve value; null/omit open | Nullable candidate |
| data.bio | string? | No current source | Never synthesize; optional omission proposal | SOURCE_REQUIRED |
| data.phone | string? | users.phone | Preserve value; PII and null/omit open | Nullable candidate |
| data.status | UserStatus | users.status | Preserve stored value | Candidate; enum members unresolved |
| data.created_at | date-time | users.created_at | ISO-8601 candidate | Legacy candidate |
| data.updated_at | date-time | users.updated_at | ISO-8601 candidate | Legacy candidate |
| data on 404/error | null by guideline | Current helper defaults absent value to {} | Do not claim endpoint output | DISCREPANCY |
| meta | object | Envelope helper | Empty object candidate | Current helper convention |
| traceId | uuid | Trace middleware | Validated or generated | Current source-backed convention |
| password_hash | Excluded | Legacy users.password_hash | Never select or return | Security boundary |

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
