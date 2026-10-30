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
Admin Bearer principal -> shared ADMIN JWT guard -> validate role/status/keyword/page -> COUNT và SELECT cùng predicates trên legacy users candidate -> map API #04 UserProfile safe fields -> PageMeta -> DESIGN_RESOURCE_RETRIEVED envelope
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

- Đọc Authorization Bearer JWT bằng shared validate_current_user_request.
- Yêu cầu role ADMIN; guard kiểm tra JWT/subject/roles trước mọi database query.
- AC-31 nói Admin có quyền user management. Checked-in schema không có permission relation; dùng claim ADMIN làm fallback permission boundary DERIVED.
- Không query user rows trước khi authorization thành công.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ, chưa hết hạn | DIRECT; shared guard. |
| JWT claims | roles | Có ADMIN sau khi normalize chữ hoa | Role requirement DIRECT; mapping permission theo claim là DERIVED. |
| Admin policy | user-management permission | ADMIN claim đại diện quyền list | DERIVED; chưa có permission table, tenant scope hoặc access audit source. |

### 0.3. Check kết quả

- Thiếu/sai Bearer/JWT: 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có ADMIN role: 403 DESIGN_ACCESS_DENIED.
- Lỗi query/mapping: 500 DESIGN_INTERNAL_ERROR.
- Page invalid: 422 DESIGN_VALIDATION_ERROR theo catalog đã đồng bộ.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. role

- Nhận query role dạng string tùy chọn.
- Khi có mặt, dùng equality users.role = :role.
- Không whitelist role vì UserRole enum members chưa được định nghĩa. Unknown value cho empty result.

### 1.2. status

- Nhận query status dạng string tùy chọn.
- Khi có mặt, dùng equality users.status = :status.
- Không whitelist status hoặc mặc định ACTIVE. Unknown value cho empty result.

### 1.3. keyword

- Dùng normalize_search_query từ app/utils/validate.py: trim, lowercase và coi blank là absent.
- Tìm substring literal trong LOWER(full_name) hoặc LOWER(email) bằng POSITION.
- Các ký tự % và _ là literal, không phải SQL pattern wildcard.

### 1.4. page

- Nhận raw query value và parse integer bằng shared parse_integer.
- Omitted page mặc định 1.
- Chỉ chấp nhận 1..2147483647; sai kiểu, <1 hoặc >int32 max trả 422 DESIGN_VALIDATION_ERROR.
- Fixed page size 20 theo API #07 precedent; không nhận size query.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Q1 — paginated user projection

Legacy users là checked-in query candidate khớp path int64 và profile API #04; live schema chưa xác minh.

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
      :keyword IS NULL
      OR POSITION(:keyword IN LOWER(u.full_name)) > 0
      OR POSITION(:keyword IN LOWER(u.email)) > 0
  )
ORDER BY u.id ASC
LIMIT :limit OFFSET :offset
~~~

- Query source hiện tại chọn safe fields; không có password_hash.
- OFFSET = (page - 1) * 20; limit = 20.
- Không join V1-PILOT UUID identity/profile/role tables.

### 2.2. Q2 — count

~~~sql
SELECT COUNT(*) AS total
FROM users AS u
WHERE (:role IS NULL OR u.role = :role)
  AND (:status IS NULL OR u.status = :status)
  AND (
      :keyword IS NULL
      OR POSITION(:keyword IN LOWER(u.full_name)) > 0
      OR POSITION(:keyword IN LOWER(u.email)) > 0
  )
~~~

Q2 dùng cùng exact predicates với Q1; result total tạo PageMeta. Hai SELECT do view gọi bằng cùng Session. Local fake DB tests không chứng minh live transaction snapshot hoặc query plan.

### 2.3. JOIN

Không có JOIN; profile projection thuộc users candidate.

### 2.4. WHERE

| Điều kiện | Predicate | Trạng thái |
|---|---|---|
| role có giá trị | users.role = :role | Query key DIRECT; exact equality DERIVED. |
| status có giá trị | users.status = :status | Query key DIRECT; exact equality DERIVED. |
| keyword sau trim không rỗng | POSITION(:keyword IN LOWER(full_name/email)) > 0 | DERIVED literal substring. |
| không có filter | Không thêm predicate tương ứng | DERIVED; không thêm deletion predicate vì schema source thiếu field. |

### 2.5. ORDER BY và phân trang

- Thứ tự users.id ASC để giữ thứ tự ổn định; không có sort query.
- Page mặc định 1, fixed size 20 theo API #07 precedent.
- Offset=(page-1)*20; total_pages=ceil(total/20), total=0 thì 0.
- Page int32 invalid trả 422; không thêm error code khác.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

API #68 là GET/read-only. Không INSERT, UPDATE, DELETE, không commit Session.

<a id="step-4-check-ket-qua-execute-query"></a>

## 4. Check kết quả execute query

### 4.1. Thành công

- Count projection phải là số nguyên không âm trong int64.
- Mỗi row phải map được vào API #04 UserProfile; id là positive int64; full_name/email/role/status là string; avatar_url/phone có thể null; timestamp cần hợp lệ.
- Response dùng Page<UserProfile>. Không có user khớp trả items=[]/total=0 HTTP 200.
- bio được omit vì không có field trong current API #04/legacy users source.

### 4.2. Lỗi hệ thống

- SQLAlchemyError, count/profile/page mapping sai trả 500 DESIGN_INTERNAL_ERROR.
- View rollback transaction lỗi và không gửi SQL, stack trace, token, password_hash hoặc profile data ra client.

### 4.3. Validate lỗi

- Page không phải integer, nhỏ hơn 1 hoặc lớn hơn int32 max trả 422 DESIGN_VALIDATION_ERROR.
- Role/status values không whitelist; khi không match, empty page là kết quả hợp lệ.

### 4.4. Ngoài trường hợp trên

- Error set direct hiện hành: 401/403/422/500.
- Không dùng 404 cho empty list.

## Request Usage Matrix

| Request field | Source | Mapping step | Query use | Response use | Basis/status |
|---|---|---|---|---|---|
| Authorization | Bearer header | 0.1/0.2 | Không đưa vào SQL | Không map | Admin guard source-backed; permission interpretation DERIVED. |
| role | Query string | 1.1 | Q1/Q2 exact predicate | Không map | Query key DIRECT. |
| status | Query string | 1.2 | Q1/Q2 exact predicate | Không map | Query key DIRECT. |
| keyword | Query string | 1.3 | Q1/Q2 normalized substring | Không map | Query key DIRECT; semantics DERIVED. |
| page | Query int32 | 1.4 | Q1 limit/offset | pagination.page | Default/range/size derived from API #07. |
| Body | None | N/A | None | None | DIRECT. |
| size/sort | Not declared | N/A | None | None | Không thêm vào request. |

## Query Matrix

| Query ID | Type | Source | Columns | Filter/order/page | Result/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy users AS u | API #04 safe UserProfile fields | Optional filters; id ASC; limit 20 | Current source; live schema unknown. |
| Q2 | COUNT | Legacy users AS u | COUNT(*) | Same predicates as Q1 | Current source; live schema unknown. |
| JOIN | N/A | N/A | None | No joins | V1-PILOT UUID rows are not used. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field/group | Type | Source | Mapping/null rule | Evidence/status |
|---|---|---|---|---|
| success/businessCode/message/meta/traceId | Envelope | Shared response/middleware | success=true; DESIGN_RESOURCE_RETRIEVED; empty meta; trace header retained | Current helper source. |
| data.items[] | UserProfile[] | Q1 users | API #04 model; optional avatar/phone serialize null; omit bio | Runtime mapped; schema candidate. |
| data.pagination.page | int32 | Validated query | Default 1 | Runtime; derived. |
| data.pagination.size | int32 | API #07 precedent | Constant 20 | Runtime; derived. |
| data.pagination.total | int64 | Q2 COUNT | Same predicates as Q1 | Runtime; legacy candidate. |
| data.pagination.total_pages | int32 | Q2 + size | Ceil; 0 for zero results | Runtime; derived. |
| email/phone | string | users.email/phone | Returned only after ADMIN guard | Reusable UserProfile; PII policy still needs owner review. |
| role/status | string | users.role/status | Stored value; exact filter; no enum whitelist | Current API #04 model uses strings; catalog enum members absent. |
| password_hash | Excluded | users.password_hash | Never selected/serialized | Verified from SQL/model source. |

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
