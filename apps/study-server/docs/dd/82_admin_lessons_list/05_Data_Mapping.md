---
title: "Data Mapping"
order: 5
dd_id: "82"
api_name: "Lấy danh sách lesson"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---
# Data Mapping

## Flow xử lý data

Raw request -> shared `ADMIN` JWT guard -> validate `course`/`type` -> bound equality filters -> read-only query candidate `lessons` -> validate từng reusable `Lesson` projection -> success envelope hoặc mapped error.

## Mục lục

- [0. Check quyền](#0-check-quyen)
- [1. Validate data input](#1-validate-data-input)
- [2. Get thông tin](#2-get-thong-tin)
- [3. Check kết quả execute query](#3-check-ket-qua-execute-query)
- [4. Map response](#4-map-response)
- [5. Trả về response](#5-tra-ve-response)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="0-check-quyen"></a>

## 0. Check quyền

### 0.1. Xác thực và authorization

- `validate_admin_request` gọi shared `validate_current_user_request(..., role="ADMIN")`.
- Guard chạy trước parse filter và DB; thiếu/sai/hết hạn credential trả 401 `DESIGN_AUTHENTICATION_REQUIRED`, principal không có role trả 403 `DESIGN_ACCESS_DENIED`.
- AC-34 nêu lesson-management permission, nhưng source hiện chỉ xác minh role `ADMIN`; không claim permission chuyên biệt.
- Không dùng filter `course` để thay authorization.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ/chưa hết hạn | Shared guard trong `app/utils/auth.py`. |
| Principal policy | Admin role | Có role `ADMIN` | Thực thi trước validation/query. |
| Admin permission | Lesson management | AC-34 precondition | Chưa có policy executable riêng. |

<a id="1-validate-data-input"></a>

## 1. Validate data input

- Raw query lấy từ `Request.query_params` để OpenAPI vẫn mô tả `course`, `status`, `type` trong khi validator sở hữu lỗi input.
- `course` parse signed int64; malformed/overflow trả HTTP 422 `DESIGN_VALIDATION_ERROR`, `meta.fieldErrors[{field:"course", code:"INT_PARSING"}]`.
- `status` được chuyển nguyên dạng; không normalize hoặc whitelist LessonStatus.
- Nếu `type` có mặt, trả HTTP 422 `DESIGN_VALIDATION_ERROR`, `meta.fieldErrors[{field:"type", code:"UNSUPPORTED_FILTER"}]`; không gọi query. Schema source không có type tương thích.
- Auth chạy trước các nhánh validation để 401/403 không bị che bởi request input.

| Input | Normalization/validation | Output |
|---|---|---|
| `course` absent | Không predicate | `course_id=None` |
| `course` signed int64 | Parse decimal signed integer | Bound integer exact match |
| `course` malformed/out-of-range | 422 `INT_PARSING` | DB không được gọi |
| `status` absent/present | Giữ nguyên string | Không predicate / exact equality |
| `type` absent | Không filter type | Tiếp tục truy vấn |
| `type` present | Không có physical mapping | 422 `UNSUPPORTED_FILTER`; DB không được gọi |

<a id="2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. SQL Q1 — read lesson list

`query.py` khai báo một SQL constant; `view.py` bind parameters và gọi `query_many`.

~~~sql
SELECT l.id, l.course_id, l.name AS title, l.content, l.video_url,
       l.sort_order AS "order", l.status
FROM lessons AS l
WHERE (:course_id IS NULL OR l.course_id = :course_id)
  AND (:status IS NULL OR l.status = :status)
ORDER BY l.course_id ASC NULLS LAST,
         l.sort_order ASC NULLS LAST,
         l.id ASC
~~~

- Legacy `lessons` BIGINT DDL là candidate read source; V1-PILOT UUID schema không được trộn vào query.
- Filter exact equality và order là DERIVED. Khi filter absent, query không loại theo course/status.
- Không join, count, pagination, page limit, deleted predicate hoặc mutation.
- SQL parameters được bind; query text không nối input.

### 2.2. Query parameters

| Parameter | Source | Meaning |
|---|---|---|
| `course_id` | Query `course` | Exact match với `lessons.course_id`, hoặc NULL để bỏ filter. |
| `status` | Query `status` | Exact match với `lessons.status`, hoặc NULL để bỏ filter. |

<a id="3-check-ket-qua-execute-query"></a>

## 3. Check kết quả execute query

- DB error hoặc projection list không đúng cấu trúc: safe HTTP 500 `DESIGN_INTERNAL_ERROR`; view gọi rollback best-effort.
- Mỗi row phải là mapping và validate thành reusable `Lesson`. Required `course_id`, `order` (`sort_order`) hoặc `status` NULL/malformed làm toàn request trả 500; không drop/default row.
- `query_many` trả `[]` là kết quả hợp lệ và đi tới success `data: []`.
- GET không commit và không có write side effect.

<a id="4-map-response"></a>

## 4. Map response

### 4.1. Lesson projection

| Contract field | Legacy candidate | Transform/behavior |
|---|---|---|
| `id` | `lessons.id` | Direct; required. |
| `course_id` | `lessons.course_id` | Direct; required by model although legacy DDL nullable. |
| `title` | `lessons.name` | Alias, consistent with API #09. |
| `content` | `lessons.content` | Direct; nullable preserved. |
| `video_url` | `lessons.video_url` | Direct; nullable preserved and validated by reusable model when present. |
| `order` | `lessons.sort_order` | Alias, required by model although legacy DDL nullable. |
| `status` | `lessons.status` | Direct; required by model although legacy DDL nullable. |

### 4.2. Collection and envelope

- Local `GetAdminLessonsEnvelope.data` là `list[Lesson]`; list shape là DERIVED từ endpoint/AC intent vì catalog schema singleton.
- Empty collection là `[]`; không trả null, singleton object, page fields hay count.
- Success: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`; shared helper tạo `meta: {}` và trace ID.
- Error helper dùng `data: null`; validation errors thêm `meta.fieldErrors`.

<a id="5-tra-ve-response"></a>

## 5. Trả về response

### 5.1. Success

- Response có `success`, `businessCode`, `message`, `data: Lesson[]`, `meta`, `traceId`.
- Không khẳng định array đã được owner phê duyệt; catalog singleton mismatch vẫn mở.

### 5.2. Errors

- 401 `DESIGN_AUTHENTICATION_REQUIRED` — thiếu/không hợp lệ Bearer credential.
- 403 `DESIGN_ACCESS_DENIED` — principal không có role `ADMIN`.
- 422 `DESIGN_VALIDATION_ERROR` — malformed/out-of-range `course` hoặc `type` filter chưa có schema mapping; local DERIVED behavior ngoài exact catalog error list.
- 500 `DESIGN_INTERNAL_ERROR` — lỗi truy vấn hoặc Lesson projection; rollback best-effort.
- Error response dùng `data: null`; validation branch có `meta.fieldErrors`.

## Request Usage Matrix

| Input | Step/use | Query/side effect | Status |
|---|---|---|---|
| Authorization Bearer | 0 | Shared ADMIN guard before validation/DB | DIRECT/local implementation |
| Admin role | 0 | Require `ADMIN` | DIRECT |
| Lesson-management permission | 0 | No separate policy check | AC-34 requirement; UNWIRED |
| `course` | 1/2 | Parse signed int64; equality on `course_id` | DERIVED |
| `status` | 1/2 | Exact equality on `status`; omitted means no predicate | DERIVED |
| `type` | 1 | Reject with 422 if present | DERIVED fallback; no source mapping |
| Page/size/sort/body | — | Not declared or consumed | Not applicable |

## Query Matrix

| Query | Operation | Tables | Conditions/order | Status |
|---|---|---|---|---|
| Q1 | Read Lesson projection | Legacy `lessons` candidate | Optional course/status filters; candidate stable order | DERIVED; live schema unverified |
| Q1 with `type` | Not executed | — | Explicit 422 unsupported filter | Local DERIVED behavior |
| Count query | None | — | No Page/count contract | Not applicable |

## Mutation Matrix

| Table/resource | Operation | Reason |
|---|---|---|
| `lessons` | None — READ ONLY | GET list; mutations belong to APIs #84–#86. |
| Audit/event tables | None evidenced | AC-34 does not assign audit write to list operation. |

## Response Source Matrix

| Response field | Source | Transform | Status/rule |
|---|---|---|---|
| Envelope fields | Reusable `ApiEnvelope<T>` | `success`, `businessCode`, `message`, `data`, `meta`, `traceId` | Direct reusable shape; list type differs from catalog declaration. |
| `data[]` | AC-34 list intent | `list[Lesson]` | DERIVED fallback; no pagination. |
| `id` | Legacy `lessons.id` | Direct | Candidate BIGINT field. |
| `course_id` | Legacy `lessons.course_id` | Direct | Required model vs nullable DDL. |
| `title` | Legacy `lessons.name` | Alias | API #09 precedent. |
| `content` | Legacy `lessons.content` | Direct | Optional, nullable preserved. |
| `video_url` | Legacy `lessons.video_url` | Direct | Optional, nullable preserved. |
| `order` | Legacy `lessons.sort_order` | Alias | API #09 precedent; source nullable. |
| `status` | Legacy `lessons.status` | Direct | Enum/casing unresolved. |

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
