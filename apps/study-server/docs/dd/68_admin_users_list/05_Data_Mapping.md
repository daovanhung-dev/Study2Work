---
title: "Data Mapping"
order: 5
dd_id: "68"
api_name: "Lấy danh sách user"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Admin Bearer principal -> xác thực role/quyền user management -> nhận filter và page -> chuẩn hóa keyword theo proposal -> Q1 đọc safe user fields, Q2 count cùng predicates -> map Page<UserProfile> candidate -> direct catalog hiện chỉ cho phép ApiEnvelope<UserProfile> -> trả 200 hoặc exact catalog errors
~~~

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Insert/Update thông tin](#step-3-insertupdate-thong-tin)
- [4. Check kết quả execute query](#step-4-check-ket-qua-execute-query)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực principal

- Đọc Authorization Bearer JWT theo requirement catalog.
- Kiểm tra role Admin và quyền user management trước khi đọc danh sách.
- Current Study guard chỉ hỗ trợ Student; không dùng lại guard đó cho API này.
- JWT claim-to-Admin identity/policy chưa có current source; cần owner xác nhận.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ, chưa hết hạn | DIRECT requirement; endpoint chưa wired. |
| JWT claims | roles | Chứa Admin theo catalog | DIRECT role; current helper/policy chưa hỗ trợ. |
| Admin policy | user-management permission | Admin được phép quản lý user | AC-31 precondition; implementation source absent. |

Không query user rows trước khi hoàn tất Admin authorization.

### 0.3. Check kết quả

- Thiếu hoặc sai Bearer credential: catalog 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có role/quyền Admin: catalog 403 DESIGN_ACCESS_DENIED.
- Không tự ánh xạ Admin role thành một bảng hay enum vật lý chưa có source.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. role

- Nhận query role dạng string tùy chọn theo catalog.
- Candidate dùng equality trên users.role khi parameter hiện diện.
- Không tạo whitelist role; tập role hợp lệ chưa được xác định.

### 1.2. status

- Nhận query status dạng string tùy chọn theo catalog.
- Candidate dùng equality trên users.status khi parameter hiện diện.
- Không tạo whitelist status hoặc mặc định ACTIVE.

### 1.3. keyword

- Nhận query keyword dạng string tùy chọn theo catalog.
- Proposal DERIVED: trim, chuyển lowercase, tìm substring trên full_name hoặc email.
- Cần xác nhận ký tự wildcard và hành vi keyword rỗng; không trả dữ liệu nhập trong lỗi.

### 1.4. page

- Nhận int32 tùy chọn theo catalog.
- Proposal DERIVED: page 1-based, omitted dùng 1, fixed size 20 theo API #07.
- Catalog không ghi minimum/default và không khai báo 422; không chốt HTTP behavior cho page <= 0 trước khi contract owner xác nhận.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query candidate — legacy users

Các truy vấn dưới đây chỉ là proposal trên legacy BIGINT schema; không khẳng định quan hệ đó là live schema.

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
WHERE (:role IS NULL OR u.role = :role)
  AND (:status IS NULL OR u.status = :status)
  AND (
      :keyword_pattern IS NULL
      OR LOWER(u.full_name) LIKE :keyword_pattern
      OR LOWER(u.email) LIKE :keyword_pattern
  )
ORDER BY u.id ASC
LIMIT :limit OFFSET :offset
~~~

- Không chọn password_hash.
- Không join identity_projections/learner_profiles từ V1-PILOT.
- keyword_pattern candidate là % + lower(keyword sau trim) + %; escaping wildcard cần được quyết định.

### 2.2. Query candidate — count

~~~sql
SELECT COUNT(*) AS total
FROM users AS u
WHERE (:role IS NULL OR u.role = :role)
  AND (:status IS NULL OR u.status = :status)
  AND (
      :keyword_pattern IS NULL
      OR LOWER(u.full_name) LIKE :keyword_pattern
      OR LOWER(u.email) LIKE :keyword_pattern
  )
~~~

Q2 dùng cùng filter với Q1. Chỉ dùng total trong candidate PageMeta; direct response hiện chưa có pagination.

### 2.3. JOIN

Không có JOIN trong candidate legacy query. Profile fields đều thuộc users. V1-PILOT cần mô hình identity/profile khác và không được nối bằng ID giả định.

### 2.4. WHERE

| Điều kiện | Candidate predicate | Trạng thái |
|---|---|---|
| Có role | users.role = :role | DERIVED exact match. |
| Có status | users.status = :status | DERIVED exact match. |
| Có keyword | LOWER(full_name) hoặc LOWER(email) chứa keyword | DERIVED; escaping/collation chưa chốt. |
| Không có filter | Không lọc theo các query trên | DERIVED; deletion visibility vẫn mở. |

### 2.5. ORDER BY và phân trang

- Candidate order users.id ASC để có thứ tự ổn định; catalog không có sort input.
- Candidate page mặc định 1; size cố định 20 theo API #07 precedent.
- offset = (page - 1) * 20 khi page hợp lệ.
- total_pages = ceil(total / 20); total=0 thì 0.
- Page<=0 và integer overflow behavior là SOURCE_REQUIRED vì catalog không nêu rule/422.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

API #68 là GET/read-only. Không có INSERT, UPDATE, DELETE, transaction mutation hoặc rollback.

<a id="step-4-check-ket-qua-execute-query"></a>

## 4. Check kết quả execute query

### 4.1. Thành công

- Candidate query hợp lệ: map từng row theo safe UserProfile projection.
- Theo proposal list, không có user phù hợp trả items=[] và total=0 với HTTP 200; cần contract correction vì response trực tiếp là một UserProfile.
- Omit bio nếu chưa có source và schema decision; không gán chuỗi rỗng.

### 4.2. Lỗi hệ thống

- Query DB hoặc mapping profile lỗi: catalog 500 DESIGN_INTERNAL_ERROR.
- Không ghi log/response raw SQL, password, credential hoặc dữ liệu PII không cần thiết.

### 4.3. Validate lỗi

- Catalog #68 không khai báo 422.
- Invalid page, unknown role/status và invalid filter handling cần contract owner quyết định; không thêm code/status trong DD direct.

### 4.4. Ngoài trường hợp trên

- Giữ exact error set 401/403/500.
- Không dùng 404 cho empty list; candidate empty collection là 200 nhưng direct response chưa có list shape.

## Request Usage Matrix

| Request field | Source | Mapping step | Candidate query use | Response use | Basis/gap |
|---|---|---|---|---|---|
| Authorization | Header Bearer | 0.1/0.2 | Không đưa vào SQL | Không map | Admin policy source absent. |
| role | Query string | 1.1 | Q1/Q2 exact predicate | Không map | Filter DIRECT; semantics DERIVED. |
| status | Query string | 1.2 | Q1/Q2 exact predicate | Không map | Filter DIRECT; values/deleted policy open. |
| keyword | Query string | 1.3 | Q1/Q2 normalized pattern | Không map | Fields/normalization DERIVED. |
| page | Query int32 | 1.4 | Q1 limit/offset | Candidate pagination.page | Default/size DERIVED; invalid input unresolved. |
| Body | None | N/A | None | None | DIRECT. |

## Query Matrix

| Query ID | Type | Source | Columns | Filter/order/page | Result/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy users AS u | Safe UserProfile fields, excluding password_hash | Optional filters; id ASC; candidate limit 20 | DERIVED legacy candidate; live schema unresolved. |
| Q2 | COUNT | Legacy users AS u | COUNT(*) | Same filters as Q1 | DERIVED; used only by candidate Page response. |
| JOIN | N/A | N/A | None | No joins | No mapping between legacy BIGINT and pilot UUID. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field/group | Type | Candidate source | Mapping/null rule | Evidence/status |
|---|---|---|---|---|
| success | boolean | Envelope branch | true success / false error | DIRECT reusable envelope. |
| businessCode | string | Catalog | Exact code per branch | DIRECT. |
| message | string | Application message | Safe localized text | Exact text not specified. |
| data.id | int64 | users.id | Direct candidate | Legacy schema candidate. |
| data.full_name | string | users.full_name | Direct candidate | API #4/#14 precedent. |
| data.email | email | users.email | Direct candidate; Admin only | PII. |
| data.role | UserRole | users.role | Direct candidate | Enum members are not listed in catalog. |
| data.avatar_url | uri? | users.avatar_url | API #4 model serializes null in current source | Optional/null contract semantics open. |
| data.bio | string? | No current source | Do not synthesize; omit only after approval | SOURCE_REQUIRED. |
| data.phone | string? | users.phone | API #4 model serializes null in current source | PII; optional/null semantics open. |
| data.status | UserStatus | users.status | Direct candidate | Enum members and deletion policy are open. |
| data.created_at | date-time | users.created_at | ISO-8601 | Legacy candidate. |
| data.updated_at | date-time | users.updated_at | ISO-8601 | Legacy candidate. |
| Candidate data.items[] | UserProfile[] | Q1 | Map safe profile per row | DERIVED; response contract mismatch. |
| Candidate data.pagination | PageMeta | Q1/Q2 | page, size=20, total, total_pages | DERIVED; approval required. |
| meta | object | Envelope helper | {} candidate | Error guideline says data null; helper uses {}. |
| traceId | uuid | Current middleware | Validated or generated | Source-backed convention. |
| password_hash | Excluded | Legacy users.password_hash | Never select/serialize | Security boundary. |

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
