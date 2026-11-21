---
title: "Data Mapping"
order: 5
dd_id: "27"
api_name: "Tìm bài tiếp theo theo curriculum"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

API #27 là GET theo API catalog. AC-15 đặt mục tiêu hiển thị điều hướng bài tiếp theo và ghi bước đọc thứ tự curriculum. Các bước dưới đây phân biệt contract trực tiếp với query candidate; không có SQL hoặc rule selection nào được chốt vì nguồn chưa định nghĩa.

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | Request header | Bearer JWT; role Student theo catalog. | Identity/access lookup chưa có predicate. | Không map vào response. | JWT claim binding và entitlement SOURCE_REQUIRED. |
| lesson_id | Path /api/v1/lessons/{lesson_id}/next | Required int64 theo catalog; min/max/positivity chưa có. | Candidate lookup lesson hiện tại; exact query chưa được runtime xác nhận. | Không map trực tiếp; làm input để tìm Lesson kế tiếp. | Invalid path mapping và current-lesson not-found semantics SOURCE_REQUIRED. |

## Query Matrix

| Query ID | Purpose | Type | Target table | Selected column | JOIN | Condition | ORDER BY | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|
| Q1 | Candidate đọc vị trí lesson hiện tại | READ — DESIGN_ONLY | lessons AS current | id | N/A | Candidate id = lesson_id; query chưa được API #27 xác nhận. | N/A | current_lesson | 2.2 |
| ↑ | Candidate đọc vị trí lesson hiện tại | READ — DESIGN_ONLY | lessons AS current | course_id | N/A | Candidate id = lesson_id; query chưa được API #27 xác nhận. | N/A | current_lesson | 2.2 |
| ↑ | Candidate đọc vị trí lesson hiện tại | READ — DESIGN_ONLY | lessons AS current | sort_order | N/A | Candidate id = lesson_id; query chưa được API #27 xác nhận. | N/A | current_lesson | 2.2 |
| ↑ | Candidate đọc vị trí lesson hiện tại | READ — DESIGN_ONLY | lessons AS current | status | N/A | Candidate id = lesson_id; query chưa được API #27 xác nhận. | N/A | current_lesson | 2.2 |
| Q2 | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | id | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | course_id | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | name | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | content | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | video_url | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | sort_order | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |
| ↑ | Candidate đọc Lesson tiếp theo | READ — DESIGN_ONLY | lessons AS next | status | N/A | SOURCE_REQUIRED — same-course, relative-order and visibility predicates are not specified. | SOURCE_REQUIRED — tie-break and exact ordering are not specified. | next_lesson | 2.3 |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| N/A | N/A — READ-ONLY | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | Không có mutation theo contract. |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Envelope | ApiEnvelope<T> schema | 4.1–4.4 | true on success; false on error | N/A | Runtime serialization chưa verify. |
| businessCode | string | Contract constant | API catalog | 4.1–4.4 | Fixed by branch | N/A | Không có gap về code list. |
| message | string | Envelope | ApiEnvelope<T> schema | 4.1–4.4 | SOURCE_REQUIRED | Text policy chưa có. | Catalog không nêu message text. |
| data.id | int64 | Candidate query result | lessons.id | 3.1 | Direct candidate mapping | Required trong Lesson | Query/projection chưa xác nhận. |
| data.course_id | int64 | Candidate query result | lessons.course_id | 3.1 | Direct candidate mapping | Required trong Lesson | Checked-in DDL nullable; live schema chưa verify. |
| data.title | string | Candidate query result | lessons.name | 3.1 | name → title | Required trong Lesson | Candidate alias theo API #9 curriculum mapping. |
| data.content | string | Candidate query result | lessons.content | 3.1 | Direct candidate mapping | Null/omit unresolved | Optional field trong Lesson. |
| data.video_url | uri | Candidate query result | lessons.video_url | 3.1 | Candidate TEXT → URI | Null/omit/conversion unresolved | Optional field trong Lesson. |
| data.order | int32 | Candidate query result | lessons.sort_order | 3.1 | sort_order → order | Required trong Lesson | Exact selection/tie-break unresolved. |
| data.status | LessonStatus | Candidate query result | lessons.status | 3.1 | Candidate direct mapping | N/A | Enum values and visibility filter unresolved. |
| meta | object | Envelope | ApiEnvelope<T> schema | 4.1–4.4 | Envelope field | Members unspecified | API-specific metadata chưa khai báo. |
| traceId | uuid | Envelope | ApiEnvelope<T> schema | 4.1–4.4 | Request correlation value | Required trong schema | API #27 trace behavior chưa runtime-verified. |

## 0. Authentication and access

### 0.1. Contract

- API catalog yêu cầu Bearer JWT và role Student.
- AC-15 precondition yêu cầu Student có quyền xem lesson.
- AC-15 diagram có bước “Kiểm tra access + trạng thái publish” trong flow xem nội dung, nhưng không mô tả predicate hoặc khẳng định bước đó nằm trong từng endpoint.
- Không suy ra claim name hoặc đọc user_id từ request.

### 0.2. Access source matrix

| Source | Data/condition | Status | Remarks |
|---|---|---|---|
| Authorization header | Bearer JWT | Contract | API #27 chưa có runtime route để xác minh authentication. |
| Student role | Role=Student | Contract | Enforcement implementation chưa có. |
| Lesson/course entitlement | User-to-course or lesson access | SOURCE_REQUIRED | Claim binding, enrollment state và prerequisite policy chưa xác định. |
| Publish visibility | Lesson/course status | SOURCE_REQUIRED | Status source, allowed values và direct-call behavior chưa xác định. |

### 0.3. Decision

- Giữ 401 DESIGN_AUTHENTICATION_REQUIRED và 403 DESIGN_ACCESS_DENIED theo catalog.
- Không tự thiết kế authorization query hoặc 403/404 masking policy.

## 1. Request validation

- lesson_id lấy từ path và có kiểu int64 bắt buộc theo catalog.
- Min/max, positivity và invalid path parse mapping chưa được contract định nghĩa.
- API #27 catalog không khai báo HTTP 422; không thêm 422 business code.
- Chi tiết chưa xác nhận ở [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-27-05-path-constraints).

## 2. Read current curriculum position and candidate next Lesson

### 2.1. Source-backed intent

- AC-15 diagram ghi API #27 GET /api/v1/lessons/{lesson_id}/next.
- AC-15 diagram ghi bước “Đọc thứ tự curriculum” sau lời gọi API.
- DB lesson design có lessons.course_id, lessons.sort_order và lessons.status.
- DB_UNICA_TABLES.md mô tả sort_order là thứ tự bài trong curriculum.
- API #9 DD có candidate curriculum ordering sort_order ASC, id ASC và filter PUBLISHED; đây là adjacent design precedent, không phải API #27 contract.

### 2.2. Q1 — Candidate current lesson lookup

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| lessons AS current | id | Candidate current lesson ID | Candidate lookup by path lesson_id; no runtime query. |
| ↑ | course_id | Candidate course scope | DDL nullable; see OPEN_QUESTIONS. |
| ↑ | sort_order | Candidate curriculum position | Does not define API #27 selection by itself. |
| ↑ | status | Candidate visibility context | No API #27 status filter confirmed. |

- Candidate predicate: current.id = lesson_id.
- This is a design candidate inferred from endpoint/path, not an approved SQL statement.
- If current lesson is absent, HTTP 404 is listed by contract, but the mapping is not verified.

### 2.3. Q2 — Candidate next Lesson lookup

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| lessons AS next | id | Candidate Lesson ID | Candidate fields from reusable Lesson schema. |
| ↑ | course_id | Course ID | Whether same-course restriction is explicit remains open. |
| ↑ | name | Lesson title source | Candidate mapping name → title. |
| ↑ | content | Optional lesson content | Null/omit mapping unresolved. |
| ↑ | video_url | Optional lesson video URI | URI conversion/null behavior unresolved. |
| ↑ | sort_order | Curriculum order | Candidate mapping sort_order → order. |
| ↑ | status | Lesson status | Enum and visibility predicate unresolved. |

**Candidate condition and ordering**

- Candidate business intent: locate a lesson following the path lesson in its curriculum.
- Same-course predicate, comparison rule, published filter, tie-break, pagination and selected-row cardinality are SOURCE_REQUIRED.
- API #9's sort_order/id ordering is reference material only; API #27 does not adopt it without confirmation.

### 2.4. Result handling

- One selected next lesson: candidate success mapping is described in 3.1; contract response is ApiEnvelope<Lesson>.
- No current lesson or no candidate next lesson: contract includes 404 DESIGN_RESOURCE_NOT_FOUND, but does not assign exact condition.
- Do not map terminal curriculum to 200 null, empty Lesson, or 404 without owner confirmation.
- Internal read/mapping error: keep 500 DESIGN_INTERNAL_ERROR from catalog.

## 3. Response mapping

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| data.id | lessons.id | Direct candidate mapping. | DESIGN_ONLY; query not verified. |
| data.course_id | lessons.course_id | Direct candidate mapping. | DDL nullability conflicts with required logical field. |
| data.title | lessons.name | Alias name → title. | Candidate precedent from API #9. |
| data.content | lessons.content | Direct candidate mapping. | Null/omit behavior unresolved. |
| data.video_url | lessons.video_url | Candidate TEXT → URI. | Null/omit/conversion unresolved. |
| data.order | lessons.sort_order | Alias sort_order → order. | Selection/tie-break unresolved. |
| data.status | lessons.status | Candidate direct mapping. | Enum values and publish filter unresolved. |

- Keep the API catalog's Lesson payload; do not add next_lesson wrapper or pagination.
- Envelope fields and error data behavior follow the reusable schema and API Guidelines.
- Response questions are tracked in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 4. Mutation and external calls

### 4.1. Database mutation

- N/A — API catalog declares GET.
- Transaction: N/A — no write operation is defined.

### 4.2. External calls

- No external API, storage access or signed URL behavior is specified for API #27.
- Do not add a call to another API based only on the AC-15 client sequence.

## 5. Return response

### 5.1. Success

- HTTP 200; businessCode DESIGN_RESOURCE_RETRIEVED.
- Return ApiEnvelope<Lesson> as declared by the API catalog.

### 5.2. Authentication and access errors

- HTTP 401 DESIGN_AUTHENTICATION_REQUIRED and HTTP 403 DESIGN_ACCESS_DENIED are catalog codes.
- Exact trigger and policy remain SOURCE_REQUIRED.

### 5.3. Not found

- HTTP 404 DESIGN_RESOURCE_NOT_FOUND is a catalog code.
- Whether it means current lesson missing, no next lesson, inaccessible lesson or another resource condition remains open.

### 5.4. System error

- HTTP 500 DESIGN_INTERNAL_ERROR.
- Do not expose raw SQL, stack trace or internal database details.

### 5.5. Links

- Request: [03_Request.md](./03_Request.md).
- Response: [04_Response.md](./04_Response.md).
- Errors: [06_Error.md](./06_Error.md).
- Open decisions: [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
---
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
