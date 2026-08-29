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
| `q` | `query["q"]` khi có | String; trim; case-fold; blank trở thành no predicate | `LOWER(c.name) LIKE '%' || q_normalized || '%'` khi có giá trị | Không map trực tiếp | Contains/case-insensitive là design-only |
| `category` | `query["category"]` khi có | Parse `int64` | Predicate deferred tới khi category–course relation có source | Không map trực tiếp | ERD chưa có relation; không tạo JOIN giả |
| `page` | `query["page"]` khi có | Parse `int32`; page phải >= 1 theo design-only rule | `OFFSET = (page - 1) * 20` | `data.pagination.page` | Default `1` design-only |
| `sort` | `query["sort"]` khi có | String; chỉ qua allow-list mapping | Safe `ORDER BY` mapping nếu được xác nhận | Không map trực tiếp | Allow-list/default order TBD |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected field | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.id` | `c.status = "PUBLISHED"` và q predicate nếu có | `published_courses` | `3.1` |
| `↑` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.name AS title` | Cùng Q1 | `published_courses` | `3.1` |
| `↑` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.description` | Cùng Q1 | `published_courses` | `3.1` |
| `↑` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.thumbnail_url` | Cùng Q1 | `published_courses` | `3.1` |
| `↑` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.price` | Cùng Q1 | `published_courses` | `3.1` |
| `↑` | Lấy trang course public theo search | `READ` | `courses AS c` | `c.status` | `c.status = "PUBLISHED"` | `published_courses` | `3.1` |
| `↑` | Lấy mentor summary | `READ` | `users AS m` | `m.id` | `m.id = c.mentor_id` | `published_courses` | `3.2` |
| `↑` | Lấy mentor summary | `READ` | `users AS m` | `m.full_name` | `m.id = c.mentor_id` | `published_courses` | `3.2` |
| `↑` | Lấy mentor summary | `READ` | `users AS m` | `m.avatar_url` | `m.id = c.mentor_id` | `published_courses` | `3.2` |
| `Q2` | Đếm tổng course public phù hợp | `READ` | `courses AS c` | `COUNT(*)` | Cùng Q1 predicates | `total_courses` | `3.3` |

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
| `data.pagination.page` | `int32` | Effective query value | `page` | `5.2` | Default `1` | `1` when omitted | Design-only default |
| `data.pagination.size` | `int32` | Design constant | `20` | `5.2` | Fixed page size | `20` | API has no `size` query |
| `data.pagination.total` | `int64` | Aggregate query | `COUNT(*)` | `5.2` | Count matching rows | `0` when empty | N/A |
| `data.pagination.total_pages` | `int32` | Derived | `total_courses`, `20` | `5.2` | `ceil(total / 20)` | `0` when total is `0` | Design-only size |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | `{}` | `{}` | N/A |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | None | `TBD — generator` | Generator TBD |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check.

## 1. Get request data

### 1.1. Get request header

- `authorization`: không bắt buộc; endpoint public.
- `content_type`: không bắt buộc vì GET không có request body.

### 1.2. Get query

- `q`: lấy từ `query["q"]` nếu được gửi.
- `category`: lấy từ `query["category"]` nếu được gửi.
- `page`: lấy từ `query["page"]` nếu được gửi; dùng `1` nếu vắng mặt.
- `sort`: lấy từ `query["sort"]` nếu được gửi.
- `page_size = 20` là biến nội bộ design-only; không nhận từ client.

## 2. Validate data input

- Validate từng query field theo [03_Request.md](./03_Request.md).
- Mỗi lỗi validation đi tới [06_Error.md](./06_Error.md#error-cases).

### 2.1. Validate `q`

- Nếu `q` không có kiểu `string`: trả `422 DESIGN_VALIDATION_ERROR`.
- Trim và case-fold `q` thành `q_normalized`.
- Nếu `q_normalized` rỗng: bỏ text predicate.

### 2.2. Validate `category`

- Nếu `category` không parse được thành `int64`: trả `422 DESIGN_VALIDATION_ERROR`.
- Nếu `category` có mặt: giữ predicate ở trạng thái `TBD`; không tạo JOIN/table/cột category giả.

### 2.3. Validate `page`

- Nếu `page` không parse được thành `int32`: trả `422 DESIGN_VALIDATION_ERROR`.
- Nếu `page < 1`: trả `422 DESIGN_VALIDATION_ERROR`.
- Nếu `page` vắng mặt: dùng `effective_page = 1`.

### 2.4. Validate `sort`

- Nếu `sort` không có kiểu `string`: trả `422 DESIGN_VALIDATION_ERROR`.
- Chỉ chuyển `sort` qua allow-list → column/direction mapping đã được xác nhận.
- Không nội suy raw `sort` vào SQL; allow-list và default order hiện là `TBD`.

## 3. Get thông tin

### 3.1. Query course page — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `↑` | `c.name AS title` | Course title | Alias theo contract `Course.title` |
| `↑` | `c.description` | Course description | Nullable |
| `↑` | `c.thumbnail_url` | Thumbnail URL | Nullable |
| `↑` | `c.price` | Course price | Serialize thành decimal string |
| `↑` | `c.status` | Course status | Filter `PUBLISHED` |
| `users AS m` | `m.id` | Mentor ID | `UserSummary` |
| `↑` | `m.full_name` | Mentor full name | `UserSummary` |
| `↑` | `m.avatar_url` | Mentor avatar URL | Nullable |

### 3.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | `N/A` | `BASE` |
| `users AS m` | `m.id = c.mentor_id` | `INNER JOIN` |

> `Course.mentor` là object bắt buộc; published course thiếu mentor tương ứng đi tới lỗi hệ thống.

### 3.3. WHERE

- `c.status = "PUBLISHED"`.
- Nếu `q_normalized` khác rỗng: `LOWER(c.name) LIKE CONCAT('%', q_normalized, '%')` với parameter binding.
- Nếu `q_normalized` rỗng: không thêm text predicate.
- Nếu `category` có mặt: category predicate chỉ được thêm sau khi source relation chính thức được xác nhận; hiện là `TBD`.

### 3.4. ORDER BY

- Nếu `sort` khớp allow-list đã xác nhận: dùng column/direction mapping tương ứng.
- Nếu `sort` không có mặt: default order chưa được contract xác nhận; không tự đặt thứ tự nghiệp vụ.

### 3.5. Pagination

- `effective_page = page` hoặc `1` nếu page vắng mặt.
- `page_size = 20`.
- `LIMIT = 20`.
- `OFFSET = (effective_page - 1) * 20`.

## 4. Get count — Q2

### 4.1. Count matching rows

- Thực hiện `COUNT(*)` trên `courses AS c`.
- Dùng cùng `PUBLISHED`, `q_normalized` và category predicate (nếu relation được xác nhận) như Q1.
- Lưu kết quả vào `total_courses`.

## 5. Check kết quả query

### 5.1. Có dữ liệu

- Nếu `published_courses` có record: tiếp tục xử lý `6`.
- Mỗi record phải có mentor để map `Course.mentor`.

### 5.2. Không có dữ liệu

- Nếu `published_courses` rỗng: trả `200` với `data.items = []`, `total = 0`, `total_pages = 0`.
- Không trả `404`; contract API #7 chỉ khai báo `200`, `422`, `500`.
- Gợi ý empty state thuộc UI flow AC-04, không thêm field vào API response.

### 5.3. Lỗi đọc hoặc map

- Nếu query, count query hoặc mapping thất bại: đi tới [06_Error.md](./06_Error.md#error-cases) với `500 DESIGN_INTERNAL_ERROR`.

## 6. Map và trả về response

### 6.1. Map từng course

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

### 6.2. Map pagination và envelope

- `data.pagination.page = effective_page`.
- `data.pagination.size = 20`.
- `data.pagination.total = total_courses`.
- `data.pagination.total_pages = ceil(total_courses / 20)`.
- `success = true`.
- `businessCode = "DESIGN_RESOURCE_RETRIEVED"`.
- `message = application success message`.
- `meta = {}`.
- `traceId = request correlation UUID`.
- Response schema: [04_Response.md](./04_Response.md).

### 6.3. Validation error

- `HTTPStatus = 422`.
- `success = false`.
- `businessCode = "DESIGN_VALIDATION_ERROR"`.
- `data = {}`.
- Chi tiết: [06_Error.md](./06_Error.md#error-cases).

### 6.4. System error

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = "DESIGN_INTERNAL_ERROR"`.
- `data = {}`.
- Không trả raw query, stack trace hoặc physical storage detail.
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
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query |  |

</details>
