---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `category` | `query["category"]` khi có | Parse `int64`; relation source TBD | Category predicate only after relation is confirmed | Không map trực tiếp | ERD chưa có category–course relation |
| `page` | `query["page"]` khi có | Parse `int32`; range/default TBD | Offset pagination | `data.pagination.page` | Contract chưa xác nhận default/range |
| `size` | `query["size"]` khi có | Parse `int32`; range/default TBD | Limit pagination | `data.pagination.size` | Contract chưa xác nhận default/range |
| `sort` | `query["sort"]` khi có | Parse `string`; allow-list TBD | Safe ORDER BY mapping only | Không map trực tiếp | Không nội suy raw query vào SQL |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected field | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Lấy trang course public | `READ` | `courses AS c` | `c.id` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `courses AS c` | `c.name AS title` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `courses AS c` | `c.description` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `courses AS c` | `c.thumbnail_url` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `courses AS c` | `c.price` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `courses AS c` | `c.status` | `c.status = "PUBLISHED"` | `published_courses` | `4.1` |
| `↑` | Lấy trang course public | `READ` | `users AS m` | `m.id` | `m.id = c.mentor_id` | `published_courses` | `4.2` |
| `↑` | Lấy trang course public | `READ` | `users AS m` | `m.full_name` | `m.id = c.mentor_id` | `published_courses` | `4.2` |
| `↑` | Lấy trang course public | `READ` | `users AS m` | `m.avatar_url` | `m.id = c.mentor_id` | `published_courses` | `4.2` |
| `Q2` | Đếm tổng course public | `READ` | `courses AS c` | `COUNT(*)` | Cùng `PUBLISHED` và filter đã áp dụng ở `Q1` | `total_courses` | `4.3` |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Query outcome | `6.1/6.2/6.3` | `true` on success | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `6.1/6.2/6.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `6.1/6.2/6.3` | Fixed by branch | Text TBD | N/A |
| `data.items[].id` | `int64` | Query result | `courses.id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].title` | `string` | Query result alias | `courses.name` | `5.1` | Alias to `title` | `N/A` | Contract/ERD naming discrepancy |
| `data.items[].description` | `string` | Query result | `courses.description` | `5.1` | Direct mapping | `null` when NULL | N/A |
| `data.items[].thumbnail_url` | `uri` | Query result | `courses.thumbnail_url` | `5.1` | Direct mapping | `null` when NULL | N/A |
| `data.items[].price` | `decimal-string` | Query result | `courses.price` | `5.1` | Serialize NUMERIC as string | `N/A` | N/A |
| `data.items[].status` | `CourseStatus` | Query result | `courses.status` | `5.1` | Direct mapping | `N/A` | Full enum catalog TBD |
| `data.items[].mentor.id` | `int64` | Joined query result | `users.id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].mentor.full_name` | `string` | Joined query result | `users.full_name` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.items[].mentor.avatar_url` | `uri` | Joined query result | `users.avatar_url` | `5.1` | Direct mapping | `null` when NULL | N/A |
| `data.items[].category` | `Category` | Unresolved source | `N/A` | `5.1` | Omit until relation confirmed | Omit | Category relation missing in ERD |
| `data.pagination.page` | `int32` | Effective query value | `page` | `5.2` | Direct/derived | `TBD` if omitted | Default TBD |
| `data.pagination.size` | `int32` | Effective query value | `size` | `5.2` | Direct/derived | `TBD` if omitted | Default TBD |
| `data.pagination.total` | `int64` | Aggregate query | `COUNT(*)` | `5.2` | Count matching rows | `0` when empty | N/A |
| `data.pagination.total_pages` | `int32` | Derived | `total`, effective `size` | `5.2` | Page-count formula | `TBD` when total/default size unresolved | Convention TBD |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | `{}` | `{}` | N/A |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | None | `TBD — generator` | Generator TBD |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `N/A` | `N/A` | `N/A` | Public endpoint; không query quyền |

### 0.3. Check kết quả

- Không áp dụng check quyền; tiếp tục xử lý `1`.

### 0.4. Get request header

- `authorization`: không bắt buộc; endpoint public và không decode Bearer token.
- `content_type`: không bắt buộc vì GET không có request body.

### 0.5. Get query data

- `category`: lấy từ `query["category"]` nếu được gửi.
- `page`: lấy từ `query["page"]` nếu được gửi.
- `size`: lấy từ `query["size"]` nếu được gửi.
- `sort`: lấy từ `query["sort"]` nếu được gửi.

## 1. Validate data input

- Validate từng query field theo [03_Request.md](./03_Request.md).
- Mỗi lỗi validation đi tới [06_Error.md](./06_Error.md#error-cases).

### 1.1. Validate `category`

- Nếu `category` không parse được thành `int64`: trả `422 DESIGN_VALIDATION_ERROR`.
- Nếu `category` được gửi nhưng chưa có relation source: giữ discrepancy/TBD, không tạo JOIN giả.

### 1.2. Validate `page`

- Nếu `page` không parse được thành `int32`: trả `422 DESIGN_VALIDATION_ERROR`.
- Default và range của `page` chưa được contract xác nhận.

### 1.3. Validate `size`

- Nếu `size` không parse được thành `int32`: trả `422 DESIGN_VALIDATION_ERROR`.
- Default và range của `size` chưa được contract xác nhận.

### 1.4. Validate `sort`

- Nếu `sort` không có kiểu `string`: trả `422 DESIGN_VALIDATION_ERROR`.
- Allow-list và mapping sort chưa được contract xác nhận; không nội suy raw value vào SQL.

## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `↑` | `c.name AS title` | Course title | Alias theo contract `Course.title` |
| `↑` | `c.description` | Course description | Nullable |
| `↑` | `c.thumbnail_url` | Thumbnail URL | Nullable |
| `↑` | `c.price` | Course price | Serialize thành decimal string |
| `↑` | `c.status` | Course status | Filter `PUBLISHED` |
| `users AS m` | `m.id` | Mentor ID | `Q1`, `UserSummary` |
| `↑` | `m.full_name` | Mentor full name | `Q1`, `UserSummary` |
| `↑` | `m.avatar_url` | Mentor avatar URL | Nullable |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | `N/A` | `BASE` |
| `users AS m` | `m.id = c.mentor_id` | `INNER JOIN` |

> `Course.mentor` là object bắt buộc trong contract; nếu dữ liệu published course thiếu mentor tương ứng, đi tới lỗi hệ thống thay vì dựng object giả.

### 2.3. WHERE

- `c.status = "PUBLISHED"`.
- Nếu `category` có mặt: áp dụng predicate chỉ sau khi category–course relation được source xác nhận; hiện ghi `TBD`.

### 2.4. ORDER BY

- Nếu `sort` có mặt: dùng mapping allow-list đã được xác nhận.
- Nếu `sort` không có mặt: thứ tự mặc định chưa được contract xác nhận; không tự đặt thứ tự nghiệp vụ.

### 2.5. Pagination

- Nếu `page` và `size` có mặt: `OFFSET = (page - 1) * size`.
- `LIMIT = size` khi `size` có mặt.
- Nếu chỉ một trong `page` hoặc `size` được gửi: effective pagination behavior là `TBD`; không tự đặt default cho biến còn thiếu.
- Default, range và empty-page convention là `TBD`; không tự gán giá trị trong DD.

## 3. Get count

### 3.1. Count matching rows

- Thực hiện `Q2` trên `courses AS c` với `COUNT(*)`.
- Dùng cùng điều kiện `c.status = "PUBLISHED"` và cùng category predicate (nếu relation được xác nhận) như `Q1`.
- Lưu kết quả vào `total_courses`.

## 4. Check kết quả query

### 4.1. Có dữ liệu

- Nếu `published_courses` có record: tiếp tục xử lý `5`.
- Mỗi record phải có mentor để map `Course.mentor`.

### 4.2. Không có dữ liệu

- Nếu `published_courses` rỗng: trả `200` với `data.items = []` và `total = 0`.
- Không trả `404` vì contract chỉ khai báo 200/422/500.

### 4.3. Lỗi đọc hoặc map

- Nếu query, count query hoặc mapping thất bại: đi tới `6.3` và [06_Error.md](./06_Error.md#error-cases).

## 5. Map response

### 5.1. Map từng course

- `data.items[].id = published_courses[].id`.
- `data.items[].title = published_courses[].name`.
- `data.items[].description = published_courses[].description`.
- `data.items[].thumbnail_url = published_courses[].thumbnail_url`.
- `data.items[].price = decimal_string(published_courses[].price)`.
- `data.items[].status = published_courses[].status`.
- `data.items[].mentor.id = published_courses[].mentor_id`.
- `data.items[].mentor.full_name = published_courses[].mentor_full_name`.
- `data.items[].mentor.avatar_url = published_courses[].mentor_avatar_url`.
- Không tạo `data.items[].category` khi chưa có source relation.

### 5.2. Map pagination

- `data.pagination.page = effective_page`.
- `data.pagination.size = effective_size`.
- `data.pagination.total = total_courses`.
- `data.pagination.total_pages = derive(total_courses, effective_size)`.
- Nếu effective page/size hoặc empty-page convention chưa xác định: giữ `TBD` trong DD.

### 5.3. Map envelope

- `success = true`.
- `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `message = application success message`.
- `meta = {}`.
- `traceId = request correlation UUID`.

## 6. Trả về response

### 6.1. Thành công

- `HTTPStatus = 200`.
- Trả `ApiEnvelope<Page<Course>>` theo [04_Response.md](./04_Response.md).

### 6.2. Validation error

- `HTTPStatus = 422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 6.3. System error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw query, stack trace hoặc internal storage detail.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

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
