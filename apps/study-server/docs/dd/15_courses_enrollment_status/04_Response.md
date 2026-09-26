---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4.1/4.2/4.3 | Fixed by branch: 200/404/500 | N/A | Protocol status. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4.1/4.2/4.3 | true on success; false on error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4.1/4.2/4.3 | Fixed by branch | N/A | Design-only code. |
| 4 | message | Message | message | string | No | N/A | N/A | 4.1/4.2/4.3 | Fixed by branch | TBD — message catalog chưa có | Không trả raw DB detail. |
| 5 | data | Enrollment | data | object | No | enrollments | N/A | 3.1/3.2 | Map thành Enrollment | {} on error | Selection predicate chưa khóa. |
| 5.1 | data.id | Enrollment ID | id | int64 | No | enrollments | id | 3.2 | Direct mapping | Required on success | Source-backed column. |
| 5.2 | data.user_id | User ID | user_id | int64 | No | enrollments | user_id | 3.2 | Direct mapping | Required on success | User identity selector chưa có. |
| 5.3 | data.course_id | Course ID | course_id | int64 | No | enrollments | course_id | 3.2 | Direct mapping | Required on success | Phải khớp path course_id. |
| 5.4 | data.status | Enrollment status | status | EnrollmentStatus | No | enrollments | status | 3.2 | Direct mapping | Required on success | Enum values chưa xác nhận. |
| 5.5 | data.enrolled_at | Enrollment time | enrolled_at | date-time | No | enrollments | enrolled_at | 3.2 | ISO-8601 serialization | Required on success | Schema NOT NULL. |
| 5.6 | data.completed_at | Completion time | completed_at | date-time | Yes | enrollments | completed_at | 3.2 | ISO-8601 serialization | null khi chưa hoàn thành | Schema nullable. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4.1/4.2/4.3 | Empty object | {} | Không thêm pagination. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4.1/4.2/4.3 | Current trace context/generator | Required in envelope | Current Study convention. |

> data chỉ được trả khi selection policy xác định được một enrollment hợp lệ. Không chọn ngẫu nhiên khi có nhiều row cùng course_id.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Enrollment status retrieved.",
  "data": {
    "id": 501,
    "user_id": 1001,
    "course_id": 101,
    "status": "ACTIVE",
    "enrolled_at": "2026-09-20T10:00:00Z",
    "completed_at": null
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

> Example chỉ minh họa shape theo Enrollment; không xác nhận cách chọn user_id trong contract Public.

## Ví dụ lỗi — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Enrollment status not found.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Enrollment status could not be retrieved.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md.
- Sheet logic: 2.Response.
