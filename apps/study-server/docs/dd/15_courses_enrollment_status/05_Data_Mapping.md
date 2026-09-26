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

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| course_id | Path /api/v1/courses/{course_id}/enrollment-status | 1.1/1.2/2.1/3.2 | Parse int64; min/max chưa đặc tả | courses.id = :course_id; enrollments.course_id = :course_id | 2.2/3.1/3.2 | data.course_id | User identity selector không nằm trong request. |

## Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Kiểm tra course tồn tại và visibility context | SELECT | courses | c | c.id | N/A | c.id = :course_id | N/A | N/A | LIMIT 1 | course_row | Không có row → candidate 404. |
| Q1 | Kiểm tra course tồn tại và visibility context | SELECT | courses | c | c.status | N/A | c.id = :course_id | N/A | N/A | LIMIT 1 | course_row | PUBLISHED predicate là derived từ AC-12. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.id | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | User identity predicate và single-row rule là SOURCE_REQUIRED. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.user_id | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | User identity predicate là SOURCE_REQUIRED. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.course_id | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | Phải khớp path course_id. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.status | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | Enum values chưa được source xác nhận. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.enrolled_at | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | Source-backed timestamp. |
| Q2 | Đọc enrollment status | SELECT | enrollments | e | e.completed_at | N/A | e.course_id = :course_id | N/A | N/A | TBD — cần selection policy | enrollment_rows | Nullable source-backed timestamp. |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A — read-only | N/A | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | Không có DB mutation. |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | Branch constant | N/A | 4.1/4.2/4.3 | true on success; false on error | N/A | N/A |
| businessCode | string | Branch constant | DESIGN_* contract code | 4.1/4.2/4.3 | Fixed by branch | N/A | Design-only code, chưa runtime catalog. |
| message | string | Branch message | Application message | 4.1/4.2/4.3 | Fixed by branch | TBD | Message catalog chưa source-backed. |
| data.id | int64 | Query result | enrollments.id | 3.2/4.1 | Direct | Required on success | Row selection unresolved. |
| data.user_id | int64 | Query result | enrollments.user_id | 3.2/4.1 | Direct | Required on success | No user identity input under Public contract. |
| data.course_id | int64 | Query result | enrollments.course_id | 3.2/4.1 | Direct | Required on success | Must match path course. |
| data.status | EnrollmentStatus | Query result | enrollments.status | 3.2/4.1 | Direct | Required on success | Enum values unresolved. |
| data.enrolled_at | date-time | Query result | enrollments.enrolled_at | 3.2/4.1 | ISO-8601 | Required on success | NOT NULL in checked-in schema. |
| data.completed_at | date-time | Query result | enrollments.completed_at | 3.2/4.1 | ISO-8601 | null when source is NULL | Nullable in checked-in schema. |
| meta | object | Envelope default | N/A | 4.1/4.2/4.3 | {} | {} | No metadata contract. |
| traceId | uuid | Trace context | Current Study middleware/envelope | 4.1/4.2/4.3 | Validated/generated UUID | Required in envelope | Current convention, API #15 unwired. |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- API là Public theo list_api.md và AC-12.
- Không đọc Authorization.
- Không decode Bearer JWT.
- Không kiểm tra role/function.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| N/A | N/A | N/A | Public endpoint; không query quyền. |

### 0.3. Check kết quả

- Không áp dụng check quyền; tiếp tục xử lý 1.

## 1. Get request data

### 1.1. Get request path

- course_id: lấy từ path /api/v1/courses/{course_id}/enrollment-status.
- Không lấy user_id từ query.
- Không lấy user_id từ header.
- Không lấy user_id từ request body.

### 1.2. Validate course_id

- Parse course_id thành int64.
- Nếu path không parse được thành int64: đi tới candidate 404 theo contract-compatible convention của API #8; cần review nếu runtime contract bổ sung 422.
- Không tự đặt min/max hoặc positive-number rule.

## 2. Get thông tin

### 2.1. Query course

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| courses AS c | c.id | Course ID | Q1 |
| ↑ | c.status | Course status | Visibility context; predicate PUBLISHED cần confirmation. |

### 2.2. Query enrollment

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| enrollments AS e | e.id | Enrollment ID | Q2 |
| ↑ | e.user_id | User ID | Source-backed nhưng không có selector từ Public request. |
| ↑ | e.course_id | Course ID | Phải khớp course_id. |
| ↑ | e.status | Enrollment status | Enum chưa khóa. |
| ↑ | e.enrolled_at | Enrollment time | Source-backed. |
| ↑ | e.completed_at | Completion time | Nullable source-backed. |

### 2.3. Điều kiện unresolved

- e.course_id = :course_id.
- User identity predicate = SOURCE_REQUIRED.
- Single-row selection rule = SOURCE_REQUIRED.
- Không chọn row đầu tiên hoặc row mới nhất khi chưa có business rule.

## 3. Check kết quả

### 3.1. Course not found

- Nếu Q1 không có record: đi tới [06_Error.md](./06_Error.md), error case 2, HTTP 404.

### 3.2. Enrollment not found or not uniquely resolvable

- Nếu Q2 không có record: đi tới [06_Error.md](./06_Error.md), error case 3, HTTP 404; semantics cần xác nhận.
- Nếu Q2 trả nhiều record và không có selection policy: dừng mapping executable và ghi SOURCE_REQUIRED.
- Không map một record tùy ý.

### 3.3. Query or mapping failure

- Nếu query hoặc mapping response thất bại: đi tới [06_Error.md](./06_Error.md), error case 4, HTTP 500.
- Không trả raw SQL, stack trace hoặc internal DB detail.

## 4. Map response

### 4.1. Map Enrollment

- data.id = enrollment_row.id.
- data.user_id = enrollment_row.user_id.
- data.course_id = enrollment_row.course_id.
- data.status = enrollment_row.status.
- data.enrolled_at = enrollment_row.enrolled_at.
- data.completed_at = enrollment_row.completed_at.
- Chỉ mapping khi selection policy đã xác định enrollment_row.

## 5. Trả về response

### 5.1. Success response

- HTTPStatus = 200.
- success = true.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- data = Enrollment theo [04_Response.md](./04_Response.md).
- meta = {}.
- traceId = current trace context.

### 5.2. Not found response

- HTTPStatus = 404.
- success = false.
- businessCode = DESIGN_RESOURCE_NOT_FOUND.
- data = {}.
- Chi tiết: [06_Error.md](./06_Error.md), error cases 1, 2 và 3.

### 5.3. System error response

- HTTPStatus = 500.
- success = false.
- businessCode = DESIGN_INTERNAL_ERROR.
- data = {}.
- Chi tiết: [06_Error.md](./06_Error.md), error case 4.

> API read-only không có BEGIN TRANSACTION, COMMIT hoặc ROLLBACK.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.
