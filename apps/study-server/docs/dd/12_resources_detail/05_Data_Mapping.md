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
| `resource_id` | `path["resource_id"]` | Parse `int64`; malformed path follows contract `404` | Q1 `resources.id` | Không map trực tiếp; dùng để lấy `data` | Positive/minimum rule chưa được source xác nhận |

## Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected column | Condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| `Q1` | Lấy resource theo ID | `READ` | `resources AS r` | `r.id` | `r.id = :resource_id` | `resource_row` | `3.2` |
| `↑` | Lấy resource theo ID | `READ` | `resources AS r` | `r.lesson_id` | `r.id = :resource_id` | `resource_row` | `3.2` |
| `↑` | Lấy resource theo ID | `READ` | `resources AS r` | `r.name` | `r.id = :resource_id` | `resource_row` | `3.2` |
| `↑` | Lấy resource theo ID | `READ` | `resources AS r` | `r.resource_type` | `r.id = :resource_id` | `resource_row` | `3.2` |
| `↑` | Lấy resource theo ID | `READ` | `resources AS r` | `r.url` | `r.id = :resource_id` | `resource_row` | `3.2` |
| `Q2` | Xác định parent course và public status | `READ` | `lessons AS l` | `l.id` | `l.id = resource_row.lesson_id` | `parent_course` | `3.3` |
| `↑` | Xác định parent course và public status | `READ` | `lessons AS l` | `l.course_id` | `l.id = resource_row.lesson_id` | `parent_course` | `3.3` |
| `↑` | Xác định parent course và public status | `READ` | `courses AS c` | `c.id` | `c.id = l.course_id` | `parent_course` | `3.3` |
| `↑` | Xác định parent course và public status | `READ` | `courses AS c` | `c.status` | `c.id = l.course_id` | `parent_course` | `3.3` |
| `Q3` | Tạo signed URL khi resource private | `EXTERNAL READ` | `Object Storage signer` | `signed_url` | `object key từ resource metadata` | `signed_url` | `4.2` |

## Query conditions

| Query ID | Clause type | Filter/condition | Remarks |
|---|---|---|---|
| `Q1` | Filter | `r.id = :resource_id` | Scope trực tiếp theo path parameter. |
| `Q2` | Join | `r.lesson_id = l.id` | Quan hệ `resources.lesson_id → lessons.id` từ ERD. |
| `Q2` | Join | `l.course_id = c.id` | Quan hệ `lessons.course_id → courses.id` từ ERD. |
| `Q2` | Filter | `c.status = 'PUBLISHED'` | Derived public-course gate; cần xác nhận trước implementation. |
| `Q3` | Branch | `resource visibility = PRIVATE` | Visibility source và storage adapter chưa được đặc tả. |
| `Q3` | Input | `object key` | Không expose object key trong response; nguồn key chưa có trong ERD. |

## Mutation Matrix

| Mutation ID | Operation | Target table/API | Record condition | Fields | Value sources | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|
| `M1` | `N/A — READ ONLY` | `N/A` | `N/A` | `N/A` | `N/A` | [07_table.md](./07_table.md) | `N/A` | Không tạo/update/delete record; signing call không phải domain mutation. |

## Response Source Matrix

| Response field | Type | Source type | Source | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `success` | `boolean` | Branch constant | Processing result | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | N/A |
| `businessCode` | `string` | Branch constant | Contract | `6.1/6.2/6.3` | Fixed `DESIGN_*` code | `N/A` | N/A |
| `message` | `string` | Branch message | Application | `6.1/6.2/6.3` | Fixed by branch | Text TBD | Message catalog chưa có |
| `data.id` | `int64` | Query result | `resources.id` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.name` | `string` | Query result | `resources.name` | `5.1` | Direct mapping | `N/A` | N/A |
| `data.type` | `ResourceType` | Query result alias | `resources.resource_type` | `5.1` | Alias `resource_type` → `type` | `N/A` | Enum catalog chưa có |
| `data.url` | `uri` | Query result or external result | `resources.url` hoặc Q3 `signed_url` | `5.1/5.2` | Direct URL for public; signed URL for private | `null` only when allowed by contract/source | Object Storage request/expiry contract TBD |
| `data.visibility` | `ResourceVisibility` | Unresolved source | `N/A — resources.visibility missing` | `5.1` | `TBD` | `TBD` | Contract field required; ERD lacks source column |
| `data.lesson_id` | `int64` | Query result | `resources.lesson_id` | `5.1` | Direct mapping | `null` when source is `NULL` | ERD marks FK `NOT NULL` |
| `meta` | `object` | Envelope default | `N/A` | `6.1/6.2/6.3` | Empty object | `{}` | N/A |
| `traceId` | `uuid` | Correlation generator | `N/A` | `6.1/6.2/6.3` | Request correlation UUID | Generator TBD | N/A |

## 0. Check quyền

### 0.1. Public endpoint

- API là public theo `list_api.md`; không bắt buộc `Authorization` và không decode Bearer token.
- AC-06/diagram có access rule cho public/private resource, nhưng nguồn không xác định carrier hoặc policy cho user đã đăng nhập.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| `N/A` | `N/A` | `N/A` | Không có permission query được khóa trong contract. |

### 0.3. Check kết quả

- Không có role/function authorization branch trong contract hiện tại; tiếp tục xử lý `1`.
- Nếu policy access được approved sau này, phải bổ sung request/auth contract và error row trước implementation.

## 1. Get request data

### 1.1. Get request path

- `resource_id`: lấy từ path parameter `/api/v1/resources/{resource_id}`.
- Request field contract chi tiết tại [03_Request.md](./03_Request.md).

### 1.2. Get request header

- `authorization`: không bắt buộc; endpoint public theo contract.
- `accept`: optional, giá trị khuyến nghị `application/json`.
- `content_type`: không bắt buộc vì GET không có request body.

## 2. Validate data input

### 2.1. Validate `resource_id`

- Parse path segment thành `int64`.
- Nếu path không parse được thành `int64`, đi tới nhánh `404 DESIGN_RESOURCE_NOT_FOUND` theo [06_Error.md](./06_Error.md#error-cases).
- Không tự đặt min/max hoặc quy tắc số dương vì contract chưa đặc tả.

## 3. Get resource và parent visibility

### 3.1. Query resource — Q1

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| `resources AS r` | `r.id` | Resource ID | `Q1` |
| `↑` | `r.lesson_id` | Lesson FK | `Q1` |
| `↑` | `r.name` | Resource name | `Q1` |
| `↑` | `r.resource_type` | Resource type | `Q1`; map sang `data.type` |
| `↑` | `r.url` | Direct/object URL | `Q1`; có thể được thay bằng signed URL |

**WHERE**

- `r.id = :resource_id`.

### 3.2. Check resource result

- Nếu Q1 không trả record: đi tới nhánh `404 DESIGN_RESOURCE_NOT_FOUND`.
- Nếu Q1 trả đúng một row: tiếp tục xử lý `3.3`.
- Nếu query trả nhiều row cho primary key `r.id`: đi tới `500 DESIGN_INTERNAL_ERROR` vì data integrity bị vi phạm.

### 3.3. Query parent course — Q2

| Target table | Join condition | Join type |
|---|---|---|
| `resources AS r` | `N/A` | `BASE RESULT FROM Q1` |
| `lessons AS l` | `l.id = r.lesson_id` | `INNER JOIN` |
| `courses AS c` | `c.id = l.course_id` | `INNER JOIN` |

**WHERE**

- `c.status = 'PUBLISHED'` — derived public-course gate.

### 3.4. Check parent result

- Nếu Q2 không trả parent lesson/course hoặc course không `PUBLISHED`: trả `404 DESIGN_RESOURCE_NOT_FOUND` theo contract public hiện tại.
- Nếu Q2 trả đúng một parent course `PUBLISHED`: tiếp tục xử lý `4`.
- Resource-level `403` theo diagram chưa được đưa vào contract; không tự phát response `403`.

## 4. Resolve URL

### 4.1. Public resource

- `visibility` phải được lấy từ approved source trước implementation; ERD hiện không có cột tương ứng.
- Nếu policy xác định resource public: `resolved_url = resource_row.url`.
- Nếu `resource_row.url` là `NULL`: giữ `data.url = null` theo optional contract field; không tự tạo URL.

### 4.2. Private resource / Object Storage signer

- Nếu policy xác định resource private và request được phép truy cập: gọi `Object Storage signer` theo adapter chưa được cung cấp.
- `object_key`: lấy từ resource metadata theo storage mapping được approved; source hiện tại chưa có field object key.
- `signed_url`: nhận từ signer và map vào `data.url`.
- Không đưa `expires_at`, credential hoặc object key vào response vì contract không định nghĩa.
- Nếu signer lỗi: dùng `500 DESIGN_INTERNAL_ERROR` vì contract API #12 không khai báo `503`.

## 5. Map response

### 5.1. Map Resource

- `data.id = resource_row.id`.
- `data.name = resource_row.name`.
- `data.type = resource_row.resource_type`.
- `data.url = resolved_url`.
- `data.visibility = TBD` cho tới khi có source `resources.visibility` hoặc policy canonical.
- `data.lesson_id = resource_row.lesson_id`.

## 6. Trả về response

### 6.1. Success response

- `HTTPStatus = 200`.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_RETRIEVED`.
- `data = Resource` theo [04_Response.md](./04_Response.md).
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
- Không trả raw SQL, stack trace, storage credential hoặc object key.
- Chi tiết lỗi: [06_Error.md](./06_Error.md#error-cases).

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Sheet logic: `3. Data mapping`.
