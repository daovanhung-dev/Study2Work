---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

## 0. Check quyền

### 0.1. Thực hiện check quyền

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có role/function authorization check.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `N/A` | `N/A` | `N/A` | Public endpoint; không query quyền |

### 0.3. Check kết quả

- Không áp dụng check quyền; tiếp tục xử lý `1`.

## 1. Get request data

### 1.1. Get request path

- `course_id`: lấy từ path parameter `/api/v1/courses/{course_id}`.
- Request field contract chi tiết tại [03_Request.md](./03_Request.md).

### 1.2. Validate `course_id`

- Parse path segment thành `int64`.
- Nếu path không parse được thành `int64`, đi tới nhánh `404` theo [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc quy tắc số dương vì contract chưa đặc tả.

## 2. Get thông tin

### 2.1. Query course detail

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `↑` | `c.name AS title` | Course title | Alias physical `name` → contract `title` |
| `↑` | `c.description` | Course description | Nullable |
| `↑` | `c.thumbnail_url` | Thumbnail URL | Nullable |
| `↑` | `c.price` | Course price | Serialize thành decimal string |
| `↑` | `c.status` | Course status | Chỉ lấy `PUBLISHED` |
| `users AS m` | `m.id` | Mentor ID | `UserSummary` |
| `↑` | `m.full_name` | Mentor full name | `UserSummary` |
| `↑` | `m.avatar_url` | Mentor avatar URL | Nullable |

### 2.2. Join mentor

| Target table | Join condition | Join type |
|---|---|---|
| `courses AS c` | `N/A` | `BASE` |
| `users AS m` | `m.id = c.mentor_id` | `INNER JOIN` |

> `Course.mentor` là object bắt buộc; không dựng mentor giả khi join không có dữ liệu.

### 2.3. Where

- `c.id = :course_id`.
- `c.status = 'PUBLISHED'`.
- Không thêm category filter, curriculum hoặc reviews vào query API #8.

### 2.4. Order

- `N/A — truy vấn theo khóa chính, trả tối đa một record`.

## 3. Check kết quả

### 3.1. Published course found

- Nếu query trả đúng một record cùng mentor: tiếp tục xử lý `4`.
- Không thực hiện count query vì response dùng singleton page.

### 3.2. Published course not found

- Nếu không có record do course không tồn tại hoặc không ở trạng thái `PUBLISHED`: trả `404 DESIGN_RESOURCE_NOT_FOUND`.
- Path sai kiểu `int64` cũng đi theo nhánh 404; không thêm 422 vì contract API #8 không khai báo.

### 3.3. Query or mapping failure

- Nếu query, join hoặc map response thất bại: đi tới nhánh `500 DESIGN_INTERNAL_ERROR`.
- Không trả raw SQL, stack trace hoặc storage detail.

## 4. Map response

### 4.1. Map singleton Page<Course>

- `data.items` chứa đúng một course record.
- `data.items[].id = course.id`.
- `data.items[].title = course.name`.
- `data.items[].description = course.description`.
- `data.items[].thumbnail_url = course.thumbnail_url`.
- `data.items[].price = decimal_string(course.price)`.
- `data.items[].status = course.status` (`PUBLISHED`).
- `data.items[].mentor.id = mentor.id`.
- `data.items[].mentor.full_name = mentor.full_name`.
- `data.items[].mentor.avatar_url = mentor.avatar_url`.
- Không map `data.items[].category` khi category–course relation chưa được source xác nhận.

### 4.2. Map singleton pagination

- `data.pagination.page = 1`.
- `data.pagination.size = 1`.
- `data.pagination.total = 1`.
- `data.pagination.total_pages = 1`.

## 5. Trả về response

### 5.1. Success response

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- `data = Page<Course>` singleton theo [04_Response.md](./04_Response.md).
- `meta = {}` và `traceId` là request correlation UUID.

### 5.2. Not found response

- `HTTPStatus = 404`.
- `success = false`.
- `businessCode = DESIGN_RESOURCE_NOT_FOUND`.
- `data = {}`.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

### 5.3. System error response

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = DESIGN_INTERNAL_ERROR`.
- `data = {}`.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

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
