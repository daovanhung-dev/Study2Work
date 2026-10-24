---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
1. Nhận Authorization Bearer và course_id:int64! theo catalog.
2. Xác thực principal Mentor và kiểm tra quyền quản lý course; guard/identity binding chưa có trong Study source.
3. Q1 candidate có thể đọc legacy courses.id/mentor_id để xác định course/direct owner; chỉ là DERIVED.
4. Q2 đọc sections/lessons/content theo AC-22 nhưng chưa có approved table/model; dừng tại SOURCE_REQUIRED, không dựng SQL.
5. Chỉ map ApiEnvelope<Content> sau khi response cardinality, Content source, payload, enums và empty-tree rule được xác nhận.
6. Success/error code giữ nguyên API catalog; endpoint hiện UNWIRED / NOT_FOUND. Error middleware fallback khi API #49 path chưa thuộc allowlist là conditional integration discrepancy.
~~~

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Yêu cầu Bearer JWT và role Mentor theo catalog.
- AC-22 yêu cầu Mentor có quyền quản lý course.
- Không nhận `mentor_id`/owner từ request; token-to-principal mapping chưa có source trong Study runtime.
- Legacy `courses.mentor_id` là candidate direct-owner check theo DD #46/#47, không đại diện course được phân công.

### 0.2. Query/check quyền

| Target | Column/field | Condition/value | Remarks |
|---|---|---|---|
| JWT principal | role | Mentor | Contract DIRECT; runtime Mentor guard `NOT_FOUND`. |
| Legacy `courses` candidate | id | bằng path `course_id` | Candidate BIGINT schema; live schema chưa xác minh. |
| Legacy `courses` candidate | mentor_id | so với numeric Mentor principal | `DERIVED`; identity mapping và assignment relation chưa có. |

### 0.3. Check kết quả

- Token thiếu/không hợp lệ: 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Role sai hoặc không có quyền quản lý course: 403 `DESIGN_ACCESS_DENIED`; ánh xạ principal/access cụ thể cần xác nhận.
- Course không tồn tại: 404 `DESIGN_RESOURCE_NOT_FOUND` là candidate theo business code; kết quả với course tồn tại nhưng content tree rỗng chưa rõ.
- Lỗi truy vấn/runtime: 500 `DESIGN_INTERNAL_ERROR`.

## 1. Validate data input

### Request Usage Matrix

| Request field | Source | Validate/use | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Header | Bearer JWT; role Mentor | Principal cho course access check | Không echo JWT/claims | Mentor guard/identity mapping `SOURCE_REQUIRED`. |
| `course_id` | Path | Required int64 theo catalog | Q1 candidate; intended scope Q2 | Candidate scope cho `Content.course_id` | Physical ID/schema unresolved; malformed path status chưa khai báo. |
| Body | N/A | N/A | N/A | N/A | Catalog không khai báo body. |
| Query | N/A | N/A | N/A | N/A | Không thêm pagination/filter/sort. |

Catalog không khai báo HTTP 422; không thêm business error cho path parse failure. Current middleware trả 422 `VALIDATION_ERROR` cho path ngoài `DESIGN_CONTRACT_PATHS`; API #49 chưa có trong allowlist nên malformed-path behavior là discrepancy có điều kiện khi future wiring.

## 2. Get thông tin

### 2.1. Query

#### Query Matrix

| Query | Type | Candidate source | Query item | Rule | Evidence/status |
|---|---|---|---|---|---|
| Q1 | SELECT | Legacy `courses AS c` | `c.id`, `c.mentor_id` | `c.id = :course_id`; compare owner with principal | Candidate legacy query; `DERIVED`, live schema/identity/assignment unresolved |
| Q2 | SELECT | No approved Content/tree relation | Base table, fields, joins, visibility and ordering unknown | Intended read by course ID from AC-22 | `SOURCE_REQUIRED`; no executable query approved |

Candidate Q1 for legacy schema only; do not treat as live query:

~~~sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :course_id;
~~~

Q2 cannot be expressed without selecting an approved schema and defining how `sections`, `lessons` and `Content` nodes relate. The V1-PILOT UUID tables are not substituted for the catalog BIGINT model.

### 2.2. JOIN

| Table | Join type | Join condition | Purpose | Evidence |
|---|---|---|---|---|
| No approved content join | N/A | N/A | Generic tree joins cannot be determined | `SOURCE_REQUIRED` |
| `courses AS c` | No join in Q1 candidate | N/A | Candidate course/direct-owner lookup | Legacy ERD/DD #46–#47; `DERIVED` |

### 2.3. WHERE

| Condition | Value source | Purpose | Evidence/status |
|---|---|---|---|
| `c.id = :course_id` | Path parameter | Candidate course lookup | `DERIVED` against legacy BIGINT schema |
| Content/course/version/status predicates | Not established | Scope and visibility of tree nodes | `SOURCE_REQUIRED`; no publish/draft filter invented |

### 2.4. ORDER BY

`SOURCE_REQUIRED` — catalog has no sort input, but ordering among sibling nodes and stable tie-breaker are not defined by source.

### Request Usage Matrix

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---:|---|---|---|---|---|
| Authorization | Header | 1 | Bearer + Mentor role | Principal in candidate Q1 access check | Access branch | No echo | Guard and identity mapping unresolved |
| `course_id` | Path | 1–2 | int64 contract | Q1 bind; Q2 intended scope | Course missing/access branch | Intended `data.course_id` | Content projection/cardinality unresolved |

### Query Matrix

| Query ID | Purpose | Type | Base table/view | Columns | JOIN | WHERE | ORDER/Pagination | Branch |
|---|---|---|---|---|---|---|---|---|
| Q1 | Candidate course existence/direct owner | SELECT | Legacy `courses` | `id`, `mentor_id` | None | `id = :course_id` | N/A | Course missing/owner mismatch; `DERIVED` |
| Q2 | Read course content tree | SELECT | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | `SOURCE_REQUIRED` | Intended course scope; exact predicate unknown | `SOURCE_REQUIRED`; no pagination contract | Mapping blocked pending schema/shape |

## 3. Insert/Update thông tin

### 3.1. Target table

N/A — read-only API.

### 3.2. Conditions

N/A — không có điều kiện ghi.

### 3.3. Items update/insert

N/A — không có INSERT/UPDATE/DELETE. API #50–#53 là các thao tác riêng trong AC-22.

### 3.4. Parameters

N/A — không có mutation parameters.

#### Mutation Matrix

| Mutation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | API #49 chỉ đọc | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

## Response Source Matrix

| Response field | Contract type | Candidate source | Transform/null rule | Status |
|---|---|---|---|---|
| `success` | boolean | Envelope branch | true for success; false for error | Envelope convention |
| `businessCode` | string | Catalog | Exact code by branch | DIRECT |
| `message` | string | Application | Safe localized text; exact copy unspecified | DERIVED |
| `data.id` | int64 | No approved Content table | No mapping | SOURCE_REQUIRED |
| `data.course_id` | int64 | Path or stored content row | Whether echoed or read from each node unresolved | SOURCE_REQUIRED |
| `data.content_type` | ContentType | No source/enum list | No transform | SOURCE_REQUIRED |
| `data.title` | string | No generic Content source | No mapping | SOURCE_REQUIRED |
| `data.payload` | object | No approved JSON schema | Do not invent members/default | SOURCE_REQUIRED |
| `data.status` | ContentStatus | No source/enum list | No visibility/member mapping | SOURCE_REQUIRED |
| `data.parent_id` | int64? | No generic parent relation | Optional field; null/omit policy unresolved | SOURCE_REQUIRED |
| `data.order` | int32 | No generic order field | Sibling ordering/ties undefined | SOURCE_REQUIRED |
| `meta` | object | Envelope | No pagination metadata defined | Null/empty serialization needs helper alignment |
| `traceId` | uuid | Request trace | Propagate request trace | Runtime route absent |

## 4. Check kết quả execute query

### 4.1. Thành công

Success is HTTP 200 `DESIGN_RESOURCE_RETRIEVED` with `ApiEnvelope<Content>` per catalog. A complete response cannot be mapped from current DB evidence. Do not publish an empty object, empty payload or empty tree as a fallback.

### 4.2. Lỗi hệ thống

DB/query/mapping failures map to 500 `DESIGN_INTERNAL_ERROR` in the catalog. Do not return SQL, schema names, stack traces or provider details.

### 4.3. Validate lỗi

HTTP 422 is not declared for API #49. The current validation handler returns 422 `VALIDATION_ERROR` for paths outside `DESIGN_CONTRACT_PATHS`; API #49 is not listed, so this is a conditional future-wiring discrepancy, not current API behavior.

### 4.4. Ngoài trường hợp trên

Do not add 409/503 or unlisted business codes. Semantics for 404 versus an existing course with no content are open questions.

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
