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
| `course_id` | Path `/api/v1/courses/{course_id}/curriculum` | Parse thành `int64`; parse failure đi tới `404` | `courses.id = :course_id`; `lessons.course_id = :course_id` | `data.items[].course_id` | Không có min/max trong contract |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected field | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Kiểm tra course public | `READ` | `courses AS c` | `c.id` | `c.id = :course_id AND c.status = 'PUBLISHED'` | `published_course` | `2.2` |
| `↑` | Kiểm tra course public | `READ` | `courses AS c` | `c.status` | `c.id = :course_id AND c.status = 'PUBLISHED'` | `published_course` | `2.2` |
| `Q2` | Lấy curriculum public | `READ` | `lessons AS l` | `l.id` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.course_id` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.name AS title` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.content` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.video_url` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.sort_order AS order` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |
| `↑` | Lấy curriculum public | `READ` | `lessons AS l` | `l.status` | `l.course_id = :course_id AND l.status = 'PUBLISHED'` | `published_lessons` | `3.2` |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete record |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Query outcome | `5.1/5.2/5.3` | `true` on success; `false` on error | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | API contract | `5.1/5.2/5.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `5.1/5.2/5.3` | Fixed by branch | Text TBD | Message catalog chưa có |
| `data.items[].id` | `int64` | Query result | `lessons.id` | `4.1` | Direct mapping | `N/A` | N/A |
| `data.items[].course_id` | `int64` | Query result | `lessons.course_id` | `4.1` | Direct mapping | `N/A` | N/A |
| `data.items[].title` | `string` | Query result alias | `lessons.name` | `4.1` | Alias `name` → `title` | `N/A` | ERD/contract naming discrepancy |
| `data.items[].content` | `string` | Query result | `lessons.content` | `4.1` | Direct mapping | `null` when source is `NULL` | Optional contract field |
| `data.items[].video_url` | `uri` | Query result | `lessons.video_url` | `4.1` | Direct mapping | `null` when source is `NULL` | Optional contract field |
| `data.items[].order` | `int32` | Query result alias | `lessons.sort_order` | `4.1` | Alias `sort_order` → `order` | `N/A` | ERD/contract naming discrepancy |
| `data.items[].status` | `LessonStatus` | Query result | `lessons.status` | `4.1` | Filter `PUBLISHED`; direct mapping | `N/A` | Enum catalog chưa đầy đủ |
| `data.pagination.page` | `int32` | Design constant | `1` | `4.2` | Fixed one-page response | `N/A` | Endpoint không nhận page |
| `data.pagination.size` | `int32` | Derived | `length(published_lessons)` | `4.2` | Số lesson trả về | `0` khi empty | One-page convention design-only |
| `data.pagination.total` | `int64` | Derived | `length(published_lessons)` | `4.2` | Số lesson public | `0` khi empty | Không cần count query riêng |
| `data.pagination.total_pages` | `int32` | Derived | `total` | `4.2` | `1` nếu total > 0, ngược lại `0` | `0` khi empty | One-page convention design-only |
| `meta` | `object` | Envelope default | `N/A` | `5.1/5.2/5.3` | Empty object | `{}` | N/A |
| `traceId` | `uuid` | Correlation generator | `N/A` | `5.1/5.2/5.3` | Request correlation UUID | `TBD — exact generator chưa đặc tả` | N/A |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo contract; không đọc hoặc decode Bearer token.
- Không có authorization query hoặc role check.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `N/A` | `N/A` | `N/A` | Public endpoint; không query quyền |

### 0.3. Check kết quả

- Không áp dụng check quyền; tiếp tục xử lý `1`.

## 1. Get request data

### 1.1. Get request path

- `course_id`: lấy từ path parameter `/api/v1/courses/{course_id}/curriculum`.
- Request field contract chi tiết tại [03_Request.md](./03_Request.md).

### 1.2. Validate `course_id`

- Parse path segment thành `int64`.
- Nếu path không parse được thành `int64`, đi tới nhánh `404` theo [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc quy tắc số dương vì contract chưa đặc tả.

## 2. Check course public

### 2.1. Query course visibility — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `courses AS c` | `c.id` | Course ID | `Q1` |
| `↑` | `c.status` | Course status | `Q1`; phải là `PUBLISHED` |

**WHERE**

- `c.id = :course_id`.
- `c.status = 'PUBLISHED'`.

### 2.2. Check result

- Nếu Q1 trả đúng một course `PUBLISHED`: tiếp tục xử lý `3`.
- Nếu Q1 không trả record: đi tới nhánh `404 DESIGN_RESOURCE_NOT_FOUND`.
- Không expose việc course tồn tại nhưng đang `DRAFT`/private cho Guest.

## 3. Get curriculum

### 3.1. Query published lessons — Q2

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `lessons AS l` | `l.id` | Lesson ID | `Q2` |
| `↑` | `l.course_id` | Course ID | `Q2` |
| `↑` | `l.name AS title` | Lesson title | Alias theo contract `Lesson.title` |
| `↑` | `l.content` | Lesson content | Nullable |
| `↑` | `l.video_url` | Lesson video URL | Nullable |
| `↑` | `l.sort_order AS order` | Lesson order | Alias theo contract `Lesson.order` |
| `↑` | `l.status` | Lesson status | Filter `PUBLISHED` |

**WHERE**

- `l.course_id = :course_id`.
- `l.status = 'PUBLISHED'`.

**ORDER BY**

- `l.sort_order ASC`.
- `l.id ASC` khi hai lesson có cùng `sort_order`.

**Pagination**

- Không nhận `page`, `size` hoặc filter từ client.
- Query lấy toàn bộ lesson public thuộc course đã được gate ở Q1.

### 3.2. Check result

- Nếu Q2 trả một hoặc nhiều record: tiếp tục xử lý `4`.
- Nếu Q2 trả `0` record: tiếp tục xử lý `4` và tạo page rỗng; không trả `404`.
- Nếu query hoặc mapping lỗi: đi tới nhánh `500 DESIGN_INTERNAL_ERROR`.

## 4. Map response

### 4.1. Map từng lesson

- `data.items[].id = published_lessons[].id`.
- `data.items[].course_id = published_lessons[].course_id`.
- `data.items[].title = published_lessons[].name`.
- `data.items[].content = published_lessons[].content`.
- `data.items[].video_url = published_lessons[].video_url`.
- `data.items[].order = published_lessons[].sort_order`.
- `data.items[].status = published_lessons[].status` (`PUBLISHED`).
- Giữ `content` và `video_url` là `null` khi giá trị nguồn là `NULL`.

### 4.2. Map pagination

- `data.pagination.page = 1`.
- `data.pagination.size = length(published_lessons)`.
- `data.pagination.total = length(published_lessons)`.
- `data.pagination.total_pages = 1` khi `length(published_lessons) > 0`.
- `data.pagination.total_pages = 0` khi `length(published_lessons) = 0`.

## 5. Trả về response

### 5.1. Success response

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- `data = Page<Lesson>` theo [04_Response.md](./04_Response.md).
- `meta = {}`.
- `traceId = request correlation UUID`.

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
<summary>Bản ghi đối chiếu</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. Check quyền |  |
| 13 | `D13` | 1. validate data input |  |
| 16 | `D16` | 2. Get thông tin |  |
| 48 | `D48` | 4. check kết quả execute query |  |

</details>
