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
| `course_id` | Path `/api/v1/courses/{course_id}/resources` | Parse thành `int64` | Q1 `courses.id`; Q2 `lessons.course_id` | Dùng để scope resource; không map trực tiếp vào `Resource` | Positive/minimum rule chưa được contract xác nhận |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected column | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Kiểm tra course public | `READ` | `courses AS c` | `c.id` | `c.id = :course_id AND c.status = 'PUBLISHED'` | `published_course` | `3.2` |
| `↑` | Kiểm tra course public | `READ` | `courses AS c` | `c.status` | `c.id = :course_id AND c.status = 'PUBLISHED'` | `published_course` | `3.2` |
| `Q2` | Scope resource theo lesson thuộc course | `READ` | `lessons AS l` | `l.id` | `l.course_id = :course_id` | `resource_rows` | `4.2` |
| `↑` | Scope resource theo lesson thuộc course | `READ` | `lessons AS l` | `l.course_id` | `l.course_id = :course_id` | `resource_rows` | `4.2` |
| `Q2` | Lấy resource metadata | `READ` | `resources AS r` | `r.id` | `r.lesson_id = l.id` | `resource_rows` | `4.2` |
| `↑` | Lấy resource metadata | `READ` | `resources AS r` | `r.lesson_id` | `r.lesson_id = l.id` | `resource_rows` | `4.2` |
| `↑` | Lấy resource metadata | `READ` | `resources AS r` | `r.name` | `r.lesson_id = l.id` | `resource_rows` | `4.2` |
| `↑` | Lấy resource metadata | `READ` | `resources AS r` | `r.resource_type` | `r.lesson_id = l.id` | `resource_rows` | `4.2` |
| `↑` | Lấy resource metadata | `READ` | `resources AS r` | `r.url` | `r.lesson_id = l.id` | `resource_rows` | `4.2` |

## Query conditions

| Query ID | Clause type | Filter/condition | Remarks |
|---|---|---|---|
| `Q1` | Filter | `c.id = :course_id` | Scope theo path parameter |
| `Q1` | Filter | `c.status = 'PUBLISHED'` | Public-course gate |
| `Q2` | Join | `r.lesson_id = l.id` | Quan hệ `resources.lesson_id → lessons.id` từ ERD |
| `Q2` | Filter | `l.course_id = :course_id` | Scope resource theo course |
| `Q2` | Gap | `N/A — resources.visibility chưa có source` | Không thêm predicate vì ERD chưa có cột `visibility` |
| `Q2` | Sort | `N/A` | Contract không đặc tả thứ tự |
| `Q2` | Pagination | `N/A` | Contract không nhận `page`/`size` và không trả `Page<Resource>` |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Query outcome | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | API contract | `6.1/6.2/6.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `6.1/6.2/6.3` | Fixed by branch | Text TBD | Message catalog chưa có |
| `data` | `object` | Query result | `resource_rows` | `5.1` | Map `Resource` theo contract | `{}` on error | Top-level cardinality chưa chốt |
| `data.id` | `int64` | Query result | `resources.id` | `5.1` | Direct mapping | `N/A` | Chưa có quy tắc chọn row nếu Q2 trả nhiều row |
| `data.name` | `string` | Query result | `resources.name` | `5.1` | Direct mapping | `N/A` | Chưa có quy tắc chọn row nếu Q2 trả nhiều row |
| `data.type` | `ResourceType` | Query result alias | `resources.resource_type` | `5.1` | Alias `resource_type` → `type` | `N/A` | Enum catalog chưa được đặc tả |
| `data.url` | `uri` | Query result | `resources.url` | `5.1` | Direct mapping | `null` khi source là `NULL`; ERD hiện ghi NOT NULL | Signed URL không thuộc API #11 |
| `data.visibility` | `ResourceVisibility` | Unresolved source | `N/A — resources.visibility missing` | `5.1` | `TBD` | `TBD — chưa chốt` | Contract bắt buộc nhưng ERD không có cột |
| `data.lesson_id` | `int64` | Query result | `resources.lesson_id` | `5.1` | Direct mapping | `null` khi source là `NULL`; ERD hiện ghi FK bắt buộc | N/A |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | N/A |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | Request correlation UUID | `TBD — exact generator chưa đặc tả` | N/A |

## 0. Check quyền

### 0.1. Public endpoint

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

- `course_id`: lấy từ path parameter `/api/v1/courses/{course_id}/resources`.
- Request field contract chi tiết tại [03_Request.md](./03_Request.md).

### 1.2. Get request header

- `authorization`: không bắt buộc; endpoint public.
- `content_type`: không bắt buộc vì GET không có request body.

## 2. Validate data input

### 2.1. Validate `course_id`

- Parse path segment thành `int64`.
- Nếu path không parse được thành `int64`, đi tới nhánh `404` theo [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc quy tắc số dương vì contract chưa đặc tả.

## 3. Check course public

### 3.1. Query course visibility — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `↑` | `c.status` | Course status | `Q1`; phải là `PUBLISHED` |

**WHERE**

- `c.id = :course_id`.
- `c.status = 'PUBLISHED'`.

### 3.2. Check result

- Nếu Q1 trả đúng một course `PUBLISHED`: tiếp tục xử lý `4`.
- Nếu Q1 không trả record: đi tới nhánh `404 DESIGN_RESOURCE_NOT_FOUND`.
- Không expose việc course tồn tại nhưng đang `DRAFT`/private cho Guest.

## 4. Get resources

### 4.1. Query resource rows — Q2

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `lessons AS l` | `l.id` | Lesson ID dùng cho join | `Q2` |
| `↑` | `l.course_id` | Course scope | `Q2` |
| `resources AS r` | `r.id` | Resource ID | `Q2` |
| `↑` | `r.lesson_id` | Lesson FK | `Q2` |
| `↑` | `r.name` | Resource name | `Q2` |
| `↑` | `r.resource_type` | Resource type | `Q2`; map sang `type` |
| `↑` | `r.url` | Resource URL | `Q2` |

**JOIN**

| Target table | Join condition | Join type |
|---|---|---|
| `lessons AS l` | `N/A` | `BASE` |
| `resources AS r` | `r.lesson_id = l.id` | `INNER JOIN` |

**WHERE**

- `l.course_id = :course_id`.
- Không thêm điều kiện `r.visibility` vì ERD không có cột này.

**ORDER BY**

- `N/A — contract không đặc tả thứ tự resource`.

**Pagination**

- `N/A — contract không nhận page/size`.

### 4.2. Check result

- Nếu Q2 không trả resource row: dùng nhánh `404 DESIGN_RESOURCE_NOT_FOUND` theo contract hiện có; việc biểu diễn empty collection `200` vẫn là `TBD` do cardinality chưa chốt.
- Nếu Q2 trả một row: tiếp tục xử lý `5`.
- Nếu Q2 trả nhiều row: giữ các row trong `resource_rows`; không tự chọn row đầu tiên và không tự đổi top-level `data` thành array/Page.
- Nếu query hoặc mapping lỗi: đi tới nhánh `500 DESIGN_INTERNAL_ERROR`.

## 5. Map response

### 5.1. Map Resource

- `data.id = resource_rows[].id` theo row được contract/cardinality chấp nhận.
- `data.name = resource_rows[].name` theo row được contract/cardinality chấp nhận.
- `data.type = resource_rows[].resource_type`.
- `data.url = resource_rows[].url`.
- `data.visibility = TBD` vì chưa có source `resources.visibility`.
- `data.lesson_id = resource_rows[].lesson_id`.
- Không tạo `signed_url`; API #12 xử lý metadata/signed URL của resource đã chọn.

> Cardinality của `data` là open question: quan hệ ERD cho phép nhiều resource nhưng catalog khai báo `ApiEnvelope<Resource>` đơn.

## 6. Trả về response

### 6.1. Success response

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- `data = Resource` theo [04_Response.md](./04_Response.md); cardinality vẫn `TBD`.
- `meta = {}`.
- `traceId = request correlation UUID`.

### 6.2. Not found response

- `HTTPStatus = 404`.
- `success = false`.
- `businessCode = DESIGN_RESOURCE_NOT_FOUND`.
- `data = {}`.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

### 6.3. System error response

- `HTTPStatus = 500`.
- `success = false`.
- `businessCode = DESIGN_INTERNAL_ERROR`.
- `data = {}`.
- Không trả raw SQL, stack trace hoặc storage detail.
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
| 4 | `D4` | 0. Check quyền |  |
| 13 | `D13` | 1. validate data input |  |
| 16 | `D16` | 2. Get thông tin |  |
| 48 | `D48` | 4. check kết quả execute query |  |

</details>
