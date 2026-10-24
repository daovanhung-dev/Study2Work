---
title: "Data Mapping"
order: 5
dd_id: "74"
api_name: "Lấy chi tiết course quản trị"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Admin Bearer principal -> kiểm tra role Admin + course-management permission -> nhận path course_id -> Q1 đọc một legacy candidate course và mentor, không lọc status -> không có row: 404 -> map Course -> bọc Page<Course> singleton -> trả 200 hoặc exact catalog errors
```

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

- Xác thực Bearer JWT và kiểm tra role Admin cùng quyền course management trước khi truy cập course data.
- Thiếu hoặc token không hợp lệ trả 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Principal không phải Admin hoặc thiếu course-management permission trả 403 `DESIGN_ACCESS_DENIED` theo catalog.
- Study hiện chỉ có Student guard; không dùng guard này thay cho Admin authorization.
- Claim role, permission policy, scope và identity mapping của Admin chưa có source; không tự tạo permission table hoặc claim name.

### 0.2. Thứ tự truy cập

- Hoàn tất authentication/authorization trước Q1.
- Không dùng response để tiết lộ course có tồn tại hay không cho caller chưa được phép.
- Không ghi audit row vì API #74 là read-only và AC-32 không chỉ định bảng/audit contract.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

### 1.1. `course_id`

- Nhận `course_id` từ path với kiểu int64 bắt buộc theo catalog.
- Không thêm minimum, maximum nghiệp vụ, enum hoặc query parameter.
- API #74 không khai báo HTTP 422; đề xuất ánh xạ path không chuyển được thành số sang 404 theo precedent validator API #08. Xác nhận overflow/ngoài miền int64 ở implementation review.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query Q1 — đọc course và mentor

- Sau khi authorization thành công, bind `course_id` vào Q1.
- Base relation candidate là legacy `courses AS c`; DDL/mapping không xác nhận live schema.
- LEFT JOIN candidate `users AS m` theo `m.id = c.mentor_id` để tạo `Course.mentor`.
- Điều kiện lọc chỉ là `c.id = :course_id`; không lọc `PUBLISHED`, vì Admin cần quản lý lifecycle trong AC-32.
- Giới hạn tối đa một row theo khóa course; không chạy count query cho Page singleton.
- Không JOIN `categories`; legacy/pilot chưa có relationship source-backed.
- AC-32 node nhắc counters; hiện response contract không nêu field/type/placement nên không truy vấn hoặc trả counter.

### 2.2. Candidate columns

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | Legacy BIGINT candidate. |
| `↑` | `c.name` | Course title | Alias response `title`. |
| `↑` | `c.description` | Course description | Nullable trong legacy DDL. |
| `↑` | `c.thumbnail_url` | Thumbnail URL | Nullable trong legacy DDL. |
| `↑` | `c.price` | Course price | NUMERIC candidate; contract yêu cầu decimal-string. |
| `↑` | `c.status` | Course status | Preserve raw; enum members chưa xác nhận. |
| `users AS m` | `m.id` | Mentor ID | `m.id = c.mentor_id`; required trong UserSummary. |
| `↑` | `m.full_name` | Mentor name | Required trong UserSummary. |
| `↑` | `m.avatar_url` | Mentor avatar | Nullable; không lấy PII khác. |

### 2.3. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | `N/A` | `BASE` |
| `users AS m` | `m.id = c.mentor_id` | `LEFT JOIN` |

> LEFT JOIN theo API #08 source giúp nhìn thấy course thiếu mentor; mapping hiện tại xem thiếu `mentor.id` hoặc `mentor.full_name` là lỗi toàn vẹn, ánh xạ candidate 500 thay vì bỏ âm thầm course.

### 2.4. WHERE / ORDER / pagination

- `c.id = :course_id`.
- Không có status predicate; public API #08 filter `PUBLISHED` không áp dụng cho Admin.
- Không cần ORDER BY/count cho khóa chính và một row.
- Khi có row, bọc Page singleton: `page=1`, `size=1`, `total=1`, `total_pages=1` (`DERIVED`).

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

### 3.1. Target table

- `N/A — READ-ONLY API`.

### 3.2. Conditions

- Không có INSERT/UPDATE/DELETE trong API #74.

### 3.3. Items update/insert

- `N/A — READ-ONLY API`; không tạo DB mutation mapping.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| `course_id` | Path `course_id` | Bind parameter cho Q1; không nội suy vào SQL. |

<a id="step-4-check-ket-qua-query"></a>

## 4. Check kết quả execute query

### 4.1. Thành công

- Q1 trả đúng một row: kiểm tra các trường bắt buộc của Course và UserSummary.
- Thiếu `mentor.id`, `mentor.full_name` hoặc `price` là candidate integrity/mapping failure và trả 500 `DESIGN_INTERNAL_ERROR` theo API #06/#08 precedent; owner cần xác nhận cách Admin xử lý course mồ côi.
- Map các trường theo [04_Response.md](./04_Response.md#response-fields).
- Không SELECT email, phone, password hash, learner count hoặc PII khác.

### 4.2. Không tìm thấy

- Q1 không có row cho `course_id`: trả 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Không áp dụng điều kiện “published”; course ở DRAFT vẫn hiện trong Admin detail.

### 4.3. Lỗi hệ thống

- Lỗi query/mapping không được trả raw SQL, stack trace hoặc credential.
- Query exception dùng 500 `DESIGN_INTERNAL_ERROR`; rollback session theo precedent API #08 khi query thất bại.

<a id="step-5-map-response"></a>

## 5. Map response

### 5.1. Map `Course`

- `items[0].id = c.id`.
- `items[0].title = c.name`.
- `items[0].description = c.description`.
- `items[0].thumbnail_url = c.thumbnail_url`.
- `items[0].price = decimal string từ c.price`, không qua float.
- `items[0].status = c.status`, giữ nguyên stored value.
- `items[0].mentor.id = m.id`.
- `items[0].mentor.full_name = m.full_name`.
- `items[0].mentor.avatar_url = m.avatar_url`.
- `items[0].category` được omit vì optional và chưa có relation source-backed.
- Nullable description/thumbnail/avatar proposal serialize `null` theo Course model hiện tại; cần chốt null-vs-omit.

### 5.2. Map `PageMeta`

- `pagination.page = 1`.
- `pagination.size = 1`.
- `pagination.total = 1`.
- `pagination.total_pages = 1`.
- Các giá trị trên chỉ dựng sau khi Q1 tìm thấy course.

### 5.3. Envelope

- Success: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `data` là singleton `Page<Course>`, `meta={}` candidate, `traceId` theo Study trace convention.
- Error: giữ chính xác các code ở [06_Error.md](./06_Error.md#error-cases); expected guideline dùng `data:null`, còn helper hiện tại mặc định `{}` khi không truyền data.

<a id="request-usage-matrix"></a>

## Request Usage Matrix

| Request item | Source | Data Mapping step | Validate | Query/mutation usage | Response usage | Gap/status |
|---|---|---|---|---|---|---|
| Authorization | Header | 0 | Bearer JWT; Admin + course-management permission | Không đưa vào SQL | Không map | Permission implementation `SOURCE_REQUIRED`. |
| `course_id` | Path | 1, 2.1 | int64 bắt buộc; không tự thêm minimum | Bind `:course_id` trong Q1 | Course ID nằm ở `items[0].id` | Invalid ID → 404 là DERIVED từ #08. |
| Request body | None | N/A | N/A | None | None | DIRECT. |
| Query parameters | None | N/A | N/A | None | None | DIRECT. |

<a id="query-matrix"></a>

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result/branch |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Đọc một course detail | SELECT | Legacy candidate `courses` | `c` | `id` | N/A | `c.id = :course_id` | N/A | N/A | Tối đa một row | Không có row → 404; có row → map Course |
| ↑ | Map title | SELECT | Legacy candidate `courses` | `c` | `name` | N/A | Cùng row Q1 | N/A | N/A | N/A | `name → title` |
| ↑ | Map description | SELECT | Legacy candidate `courses` | `c` | `description` | N/A | Cùng row Q1 | N/A | N/A | N/A | Nullable candidate |
| ↑ | Map thumbnail | SELECT | Legacy candidate `courses` | `c` | `thumbnail_url` | N/A | Cùng row Q1 | N/A | N/A | N/A | Nullable candidate |
| ↑ | Map price | SELECT | Legacy candidate `courses` | `c` | `price` | N/A | Cùng row Q1 | N/A | N/A | N/A | decimal-string; NULL → candidate 500 |
| ↑ | Map status | SELECT | Legacy candidate `courses` | `c` | `status` | N/A | Không lọc status | N/A | N/A | N/A | Preserve raw stored value |
| Q1 | Join mentor ID | LEFT JOIN | Legacy candidate `users` | `m` | `id` | `m.id = c.mentor_id` | N/A | N/A | N/A | N/A | Required `UserSummary.id` |
| ↑ | Join mentor name | SELECT | Legacy candidate `users` | `m` | `full_name` | Cùng join Q1 | N/A | N/A | N/A | N/A | Required `UserSummary.full_name` |
| ↑ | Join mentor avatar | SELECT | Legacy candidate `users` | `m` | `avatar_url` | Cùng join Q1 | N/A | N/A | N/A | N/A | Optional, null candidate |
| Q-category | Chưa có relation | N/A | N/A | N/A | N/A | Không có JOIN | N/A | N/A | N/A | N/A | `SOURCE_REQUIRED`; optional response field omit |
| Q-counters | Chưa có output field | N/A | N/A | N/A | N/A | Chưa có query | N/A | N/A | N/A | N/A | AC-32 diagram nhắc counters; giữ open question |

<a id="mutation-matrix"></a>

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | None | N/A | API read-only | No mutation fields | N/A | N/A | [07_table.md](./07_table.md) đánh dấu N/A | No transaction/commit | Query error → catalog 500 |

<a id="response-source-matrix"></a>

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty/omit rule | Gap/status |
|---|---|---|---|---|---|---|---|
| `success` | boolean | Envelope | Branch | 5.3 | true/false | N/A | DIRECT convention. |
| `businessCode` | string | Catalog | API #74 codes | 5.3 | Exact branch code | N/A | DIRECT. |
| `message` | string | Application | Safe localized text | 5.3 | No raw DB message | Text unspecified | DERIVED. |
| `data.items[]` | `Course[]` | Query result | Q1 | 4.1/5.1 | Singleton array | Exactly one row on success | DIRECT type; singleton DERIVED. |
| `data.items[].id` | int64 | Direct DB | `courses.id` | 5.1 | Copy | Required | Legacy candidate. |
| `data.items[].title` | string | Direct DB/alias | `courses.name` | 5.1 | Alias `name → title` | Required | #06/#08 precedent. |
| `data.items[].description` | string? | Direct DB | `courses.description` | 5.1 | Copy | Null candidate | #08 model precedent; confirm. |
| `data.items[].thumbnail_url` | uri? | Direct DB | `courses.thumbnail_url` | 5.1 | Copy | Null candidate | #08 model precedent; confirm. |
| `data.items[].price` | decimal-string | Direct DB/transform | `courses.price` | 5.1 | Exact decimal format, no float | NULL → candidate 500 | Required contract; nullable DDL conflict. |
| `data.items[].status` | CourseStatus | Direct DB | `courses.status` | 5.1 | Preserve value | All statuses, no filter | Enum members/casing open. |
| `data.items[].mentor.id` | int64 | Direct DB via join | `users.id` | 5.1 | Copy | Required; missing → candidate 500 | Legacy relation candidate. |
| `data.items[].mentor.full_name` | string | Direct DB via join | `users.full_name` | 5.1 | Copy | Required; missing → candidate 500 | Legacy relation candidate. |
| `data.items[].mentor.avatar_url` | uri? | Direct DB via join | `users.avatar_url` | 5.1 | Copy | Null candidate | #08 model precedent. |
| `data.items[].category` | `Category?` | No approved source | N/A | N/A | N/A | Omit; optional | `SOURCE_REQUIRED`. |
| `data.pagination.page` | int32 | Calculated/fixed | Singleton Page | 5.2 | Fixed `1` | `1` | DERIVED. |
| `data.pagination.size` | int32 | Calculated/fixed | Singleton Page | 5.2 | Fixed `1` | `1` | DERIVED. |
| `data.pagination.total` | int64 | Calculated/fixed | Q1 row existence | 5.2 | Fixed `1` | `1` | DERIVED. |
| `data.pagination.total_pages` | int32 | Calculated/fixed | Singleton Page | 5.2 | Fixed `1` | `1` | DERIVED. |
| `data.counters` | Not contracted | No source/field definition | N/A | N/A | N/A | Not emitted | AC-32 diagram vs response schema discrepancy. |
| `meta` | object | Envelope convention | N/A | 5.3 | Empty object candidate | `{}` | Current helper convention. |
| `traceId` | uuid | Middleware | Current request trace | 5.3 | Propagate/generate | Valid UUID | Current source convention. |

## Error linkage

- Authentication, authorization, not-found và internal error branches xem [06_Error.md](./06_Error.md#error-cases).
- API #74 chưa wired; `DESIGN_CONTRACT_PATHS` hiện chưa chứa route detail này.
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
