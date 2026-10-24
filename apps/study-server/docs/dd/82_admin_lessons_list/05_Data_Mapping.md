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

Admin Bearer JWT -> xác thực role/permission -> parse `course`, `status`, `type` -> truy vấn lesson theo filter đã được duyệt -> map reusable Lesson -> 200 hoặc exact catalog errors.

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

- Xác thực Bearer JWT và yêu cầu role Admin theo catalog.
- Yêu cầu thêm quyền lesson management theo tiền điều kiện AC-34.
- Token thiếu/sai/không hợp lệ -> HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal thiếu role/quyền -> HTTP 403 `DESIGN_ACCESS_DENIED`.
- Current `app/utils/auth.py` chỉ xác thực Student; Admin claim, permission source và guard chưa có.
- Không truy vấn `lessons` trước khi authorization thành công; không dùng query `course` để thay permission.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer credential | Token hợp lệ/chưa hết hạn | DIRECT requirement; endpoint chưa wired. |
| Principal policy | Admin role | Principal có Admin role | DIRECT theo catalog; claim source chưa có. |
| Admin permission | lesson management | Được cấp quyền quản lý bài học | AC-34 precondition; implementation SOURCE_REQUIRED. |

<a id="1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `course`

- Query tùy chọn kiểu int64 theo catalog.
- Exact match `lessons.course_id = :course` là mapping proposal `DERIVED`; cột được thấy trong legacy DDL, nhưng live schema chưa được xác nhận.
- Không thêm positive range, existence hoặc ownership validation nếu chưa có contract.

### 1.2. `status`

- Query tùy chọn kiểu string theo catalog.
- Nếu có, exact match `lessons.status = :status` là proposal; nếu vắng mặt, không thêm status predicate để Admin có thể xem mọi status.
- Không mặc định `PUBLISHED`, không normalize casing và không dựng enum allowlist. LessonStatus members/casing chưa đầy đủ.

### 1.3. `type`

- Query tùy chọn kiểu string là DIRECT.
- Không tìm thấy field type trong reusable Lesson, legacy `lessons`, hoặc V1-PILOT `lessons`.
- Không map sang loại resource/content block và không bỏ qua query khi được gửi.
- Cần owner xác định field/relation, các giá trị hợp lệ và semantics trước khi chốt physical query (`SOURCE_REQUIRED`).

### 1.4. Query không được khai báo

- Không nhận `page`, `size`, `sort` hay body.
- Catalog không chỉ định HTTP 400/422 cho malformed query. Cần đồng bộ parser/middleware để không trả generic validation code ngoài direct error set.

<a id="2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Candidate query trên legacy DDL

SQL dưới đây chỉ là candidate khi API contract/schema và semantics `course`/`status` được xác nhận. Không chạy như live query đã kiểm chứng.

~~~sql
SELECT
    l.id,
    l.course_id,
    l.name AS title,
    l.content,
    l.video_url,
    l.sort_order AS "order",
    l.status
FROM lessons AS l
WHERE (:course IS NULL OR l.course_id = :course)
  AND (:status IS NULL OR l.status = :status)
ORDER BY l.course_id ASC, l.sort_order ASC, l.id ASC
~~~

- Query `type` chưa được đưa vào vì thiếu field/predicate nguồn. Khi client gửi `type`, không được chạy candidate query trên đây như thể filter đã áp dụng.
- Nếu collection response được duyệt, SQL trên trả mọi row khớp; không thêm pagination/limit chưa được đặc tả. Response cap/workload cần quyết định riêng.
- Dùng bound parameters; không nối giá trị request vào câu SQL.
- `course_id` có thể NULL theo legacy DDL nhưng là required trong reusable Lesson. Không thêm `IS NOT NULL` để che row lỗi; cách xử lý cần được chốt.

### 2.2. Candidate mapping

| Logical field | Legacy physical field | Transform | Status |
|---|---|---|---|
| `id` | `lessons.id` | Direct | Candidate BIGINT mapping. |
| `course_id` | `lessons.course_id` | Direct | Nullable DDL vs required contract discrepancy. |
| `title` | `lessons.name` | Alias `name -> title` | API #09 precedent. |
| `content` | `lessons.content` | Direct | Optional contract field. |
| `video_url` | `lessons.video_url` | Direct | Optional contract field. |
| `order` | `lessons.sort_order` | Alias `sort_order -> order` | API #09 precedent. |
| `status` | `lessons.status` | Direct | Enum/casing unresolved. |
| `type` | No compatible field | None | SOURCE_REQUIRED. |

### 2.3. Schema choice

- Legacy `DB.sql` uses BIGINT lesson/course identifiers and columns compatible with most reusable Lesson fields.
- V1-PILOT uses UUID lesson IDs tied to chapter/course version and has no matching `course_id`, `status`, or `type` set.
- These models are not interchangeable. Live schema/target model selection is `SOURCE_REQUIRED`; do not join or cast them into one representation.

<a id="3-check-ket-qua-execute-query"></a>

## 3. Check kết quả execute query

### 3.1. Có dữ liệu

- Chỉ map khi mọi field required (`id`, `course_id`, `title`, `order`, `status`) có thể đáp ứng contract.
- Nếu legacy row có `course_id=NULL`, không thể serialize thành reusable Lesson theo schema hiện tại; không tự thay NULL bằng 0 hoặc bỏ row.
- Query/database/mapping failure dùng 500 `DESIGN_INTERNAL_ERROR`; không trả SQL hoặc stack trace.

### 3.2. Không có dữ liệu

- Catalog chỉ nói `ApiEnvelope<Lesson>`, không quy định empty list.
- Nếu owner duyệt collection proposal, kết quả rỗng nên là 200 `DESIGN_RESOURCE_RETRIEVED` với `data: []` (`DERIVED`). Không trả 404 cho collection rỗng nếu dùng collection contract.
- Singleton contract không định nghĩa empty result; cần owner quyết định.

<a id="4-map-response"></a>

## 4. Map response

### 4.1. Direct catalog model

Map đúng bảy field của reusable `Lesson`; không thêm `type`, created/updated timestamps, resources, progress, page metadata hoặc audit metadata.

### 4.2. Collection proposal

Nếu list cardinality được xác nhận, bọc danh sách Lesson trực tiếp trong `data` (`Lesson[]`). Không tự thêm `{items,pagination}` vì catalog không khai báo `Page<Lesson>`.

### 4.3. Envelope

- Success dùng HTTP 200 và `DESIGN_RESOURCE_RETRIEVED`.
- Error code chỉ được phép dùng 401/403/500 như catalog; middleware path chưa allowlist #82.
- Guideline error envelope quy định `data:null`, còn helper hiện tại mặc định `{}` khi không truyền data. Đây là integration gap; chưa có runtime #82 behavior.

<a id="5-tra-ve-response"></a>

## 5. Trả về response

### 5.1. Success

- Trả response sau khi query và mapping thành công.
- Message và meta conventions chưa được #82/source chỉ rõ; dùng envelope convention khi tích hợp, không thêm business field.

### 5.2. Errors

- 401 `DESIGN_AUTHENTICATION_REQUIRED` — thiếu/không hợp lệ Bearer credential.
- 403 `DESIGN_ACCESS_DENIED` — không có role Admin hoặc permission.
- 500 `DESIGN_INTERNAL_ERROR` — lỗi truy vấn/mapping không xử lý được.
- Query parse errors và filter `type` chưa có contract behavior phù hợp; cần giải quyết trước khi tuyên bố implementation hoàn chỉnh.

## Request Usage Matrix

| Input | Step/use | Query/side effect | Status |
|---|---|---|---|
| Authorization Bearer | 0 | Authenticate only | DIRECT |
| Admin role | 0 | Authorize before DB read | DIRECT |
| Lesson-management permission | 0 | Authorize before DB read | DIRECT from AC-34 |
| `course` | 1/2 | Candidate equality on `course_id` | DERIVED physical mapping |
| `status` | 1/2 | Candidate equality on `status`; omitted = no status predicate | DERIVED |
| `type` | 1/2 | Intended filter, physical target unknown | SOURCE_REQUIRED |
| Path/body/pagination/sort | — | Not declared | Not accepted by this contract |

## Query Matrix

| Query | Operation | Tables | Conditions/order | Status |
|---|---|---|---|---|
| Q1 | Read lesson projection | Legacy `lessons` candidate | Optional course/status predicates; candidate `course_id, sort_order, id` order | DERIVED; no live schema proof |
| Q1 with `type` | No approved candidate | Unknown | Must not silently ignore filter | SOURCE_REQUIRED |
| Count query | None | — | No Page/count contract | Not applicable |

## Mutation Matrix

| Table/resource | Operation | Reason |
|---|---|---|
| `lessons` | None — READ ONLY | GET list; mutations are separate APIs #84–#86. |
| Audit/event tables | None evidenced | AC-34 does not assign audit write to list operation. |

## Response Source Matrix

| Response field | Source | Transform | Status/rule |
|---|---|---|---|
| Envelope fields | Catalog reusable `ApiEnvelope<T>` | `success`, `businessCode`, `message`, `data`, `meta`, `traceId` | Direct reusable shape; error data helper mismatch unresolved. |
| `id` | Legacy `lessons.id` | Direct | Candidate BIGINT field. |
| `course_id` | Legacy `lessons.course_id` | Direct | Required contract vs nullable DDL discrepancy. |
| `title` | Legacy `lessons.name` | Alias | API #09 precedent. |
| `content` | Legacy `lessons.content` | Direct | Optional field. |
| `video_url` | Legacy `lessons.video_url` | Direct | Optional field. |
| `order` | Legacy `lessons.sort_order` | Alias | API #09 precedent. |
| `status` | Legacy `lessons.status` | Direct | Enum/casing unresolved. |
| `type` | No source | None | Not in Lesson response; query behavior still unresolved. |
| Collection wrapper | AC-34 list intent | Proposed `Lesson[]` | DERIVED; conflicts with direct singleton response. |

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
